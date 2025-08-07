import time
import os
<<<<<<< HEAD
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# === Set up Selenium ===
service = Service(executable_path="/usr/local/bin/chromedriver")  # replace with path to your chromedriver
=======
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# === STEP 1: Set up Selenium Chrome Driver ===
service = Service(executable_path="/usr/local/bin/chromedriver")  # Adjust path as needed
>>>>>>> bc10430 (Zoom out and take screenshots of each tab)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

<<<<<<< HEAD
# === Go to NetSuite saved search URL ===
netsuite_url = "https://td3019885.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=FxReval&whence="
driver.get(netsuite_url)
time.sleep(20)  # Wait for you to log in manually

# === Google Drive Auth ===
=======
# === STEP 2: Go to NetSuite Saved Search Page ===
netsuite_url = "https://td3019885.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=FxReval&whence="
driver.get(netsuite_url)
time.sleep(20)  # Give you time to manually log in

# === STEP 3: Authorize Google Drive Upload ===
>>>>>>> bc10430 (Zoom out and take screenshots of each tab)
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

<<<<<<< HEAD
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
=======
# === STEP 4: Find Record Links ===
wait = WebDriverWait(driver, 10)
base_url = "https://td3019885.app.netsuite.com"
record_links = driver.find_elements(By.CSS_SELECTOR, "a.dottedlink.viewitem")

# === STEP 5: Loop through each record link ===
for i, link in enumerate(record_links):
    try:
        href = link.get_attribute('href')
        full_url = href if href.startswith('http') else base_url + href

        # Open record in a new tab
        driver.execute_script("window.open(arguments[0]);", full_url)
        driver.switch_to.window(driver.window_handles[1])  # Switch to new tab

        # Wait for page to load and identify readonly fields
>>>>>>> bc10430 (Zoom out and take screenshots of each tab)
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.uir-field.inputreadonly"))
        )

<<<<<<< HEAD
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

=======
        # Print all fields to identify document number
        for idx, el in enumerate(elements):
            print(f"Element {idx}: '{el.text.strip()}'")

        document_number = elements[1].text.strip()  # Update index if needed
        print(f"Using document number: {document_number}")

        # === STEP 6: Click All Tabs, Take Screenshots ===
        tabs = driver.find_elements(By.CSS_SELECTOR, 'a.formtabtext[data-nsps-type="tab"]')

        for j, tab in enumerate(tabs):
            try:
                tab_name = tab.get_attribute('data-nsps-label') or f"tab{j+1}"
                driver.execute_script("arguments[0].scrollIntoView();", tab)
                tab.click()
                time.sleep(2)  # wait for tab to load

                # === Zoom out until everything fits on screen ===
                while True:
                    scroll_height = driver.execute_script("return document.body.scrollHeight")
                    window_height = driver.execute_script("return window.innerHeight")
                    if scroll_height <= window_height:
                        break
                    driver.execute_script("document.body.style.zoom = (parseFloat(document.body.style.zoom || '1') - 0.1).toString();")
                    time.sleep(0.5)

                # Take screenshot
                screenshot_name = f"CR#{document_number}.{j+1}_{tab_name}.png"
                screenshot_path = os.path.join(os.getcwd(), screenshot_name)
                driver.execute_script("document.body.style.zoom='0.5'")
                time.sleep(2)
                driver.save_screenshot(screenshot_path)

                # Upload to Google Drive
                file = drive.CreateFile({'title': screenshot_name, 'parents': [{'id': '1isdT9T7TKOxR3BpnFzITjj_fYMDStg9y'}]})
                file.SetContentFile(screenshot_path)
                file.Upload()
                print(f"Uploaded {screenshot_name}")

                # Optional: delete local file after upload
                os.remove(screenshot_path)

                # Reset zoom back to 100% before next tab
                driver.execute_script("document.body.style.zoom = '1'")

            except Exception as e:
                print(f"Error capturing tab {j+1} of record {document_number}: {e}")

        # === STEP 7: Close tab and return to main window ===
>>>>>>> bc10430 (Zoom out and take screenshots of each tab)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    except Exception as e:
        print(f"Error with record {i+1}: {e}")

<<<<<<< HEAD

=======
# === STEP 8: Done! Quit browser ===
>>>>>>> bc10430 (Zoom out and take screenshots of each tab)
driver.quit()
