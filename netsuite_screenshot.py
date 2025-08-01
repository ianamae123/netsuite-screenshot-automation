import time
import os
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# === Set up Selenium ===
service = Service(executable_path="/usr/local/bin/chromedriver")  # replace with path to your chromedriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

# === Go to NetSuite saved search URL ===
netsuite_url = "https://td3019885.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=FxReval&whence="
driver.get(netsuite_url)
time.sleep(20)  # Wait for you to log in manually

# === Google Drive Auth ===
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# === Find all record links on the page ===
record_links = driver.find_elements(By.CSS_SELECTOR, "a.d1")  # adjust selector if needed

# === Loop through records ===
base_url = "https://td3019885.app.netsuite.com"
record_links = driver.find_elements(By.CSS_SELECTOR, "a.dottedlink.viewitem")

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

for i, link in enumerate(record_links):
    try:
        href = link.get_attribute('href')
        if href.startswith('http'):
            full_url = href
        else:
            full_url = base_url + href

        driver.execute_script("window.open(arguments[0]);", full_url)
        driver.switch_to.window(driver.window_handles[1])

        # Wait for the page to load and the elements to appear
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.uir-field.inputreadonly"))
        )

        # Print all candidate elements to find the right one
        for idx, el in enumerate(elements):
            print(f"Element {idx}: '{el.text.strip()}'")

        # Choose the right element index based on output (start with 0)
        document_number = elements[1].text.strip()  # Adjust the index if needed
        print(f"Using document number: {document_number}")

        filename = f"CR#{document_number}.png"
        filepath = os.path.join(os.getcwd(), filename)
        driver.save_screenshot(filepath)

        file = drive.CreateFile({'title': filename, 'parents': [{'id': '1isdT9T7TKOxR3BpnFzITjj_fYMDStg9y'}]})
        file.SetContentFile(filepath)
        file.Upload()

        print(f"Uploaded {filename}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    except Exception as e:
        print(f"Error with record {i+1}: {e}")


driver.quit()
