import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# === Set up Selenium ===
service = Service(executable_path="/usr/local/bin/chromedriver")  # adjust path if needed
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

# === STEP 2: Go to NetSuite Saved Search Page ===
netsuite_url = "https://td3019885.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=FxReval&whence="
driver.get(netsuite_url)
time.sleep(20)  # Give you time to manually log in

# === STEP 3: Authorize Google Drive Upload ===
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# === STEP 4: Find Record Links ===
wait = WebDriverWait(driver, 10)
base_url = "https://td3019885.app.netsuite.com"
record_links = driver.find_elements(By.CSS_SELECTOR, "a.dottedlink.viewitem")

# === STEP 5: Loop through each record link ===
for i, link in enumerate(record_links):
    document_number = f"unknown_{i+1}"  # in case it fails early
    try:
        href = link.get_attribute('href')
        full_url = href if href.startswith('http') else base_url + href

        # Open record in a new tab
        driver.execute_script("window.open(arguments[0]);", full_url)
        driver.switch_to.window(driver.window_handles[1])  # Switch to new tab

        # Wait for page to load and identify readonly fields
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.uir-field.inputreadonly"))
        )

        # Getting document number
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
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    except Exception as e:
        print(f"Error with document number {document_number}: {e}")

# === STEP 8: Done! Quit browser ===
driver.quit()
