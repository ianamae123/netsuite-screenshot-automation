import time
import os
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# === CONFIG ===
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
NETSUITE_URL = "https://td3019885.app.netsuite.com/app/accounting/transactions/transactionlist.nl?Transaction_TYPE=FxReval&whence="
DRIVE_FOLDER_ID = "1isdT9T7TKOxR3BpnFzITjj_fYMDStg9y"  # Google Drive folder ID

# === Set up Selenium ===
service = Service(executable_path=CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

# === STEP 2: Go to NetSuite Saved Search Page ===
driver.get(NETSUITE_URL)
time.sleep(20)  # time alotted to log in manually

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
    document_number = f"unknown_{i+1}"
    try:
        href = link.get_attribute('href')
        full_url = href if href.startswith('http') else base_url + href

        # Open record in a new tab
        driver.execute_script("window.open(arguments[0]);", full_url)
        driver.switch_to.window(driver.window_handles[1])

        # Wait for page to load
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.uir-field.inputreadonly"))
        )

        # Get document number
        document_number = elements[1].text.strip()
        print(f"Using document number: {document_number}")

        # Loop through all tabs
        tabs = driver.find_elements(By.CSS_SELECTOR, 'a.formtabtext[data-nsps-type="tab"]')
        for j, tab in enumerate(tabs):
            try:
                tab_name = tab.get_attribute('data-nsps-label') or f"tab{j+1}"
                driver.execute_script("arguments[0].scrollIntoView();", tab)
                tab.click()
                time.sleep(2)  # wait for tab to load

                # === Print full page to PDF ===
                pdf_name = f"CR#{document_number}.{j+1}_{tab_name}.pdf"
                pdf_path = os.path.join(os.getcwd(), pdf_name)
                pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
                with open(pdf_path, "wb") as f:
                    f.write(base64.b64decode(pdf_data['data']))

                # === Upload PDF to Google Drive ===
                file = drive.CreateFile({'title': pdf_name, 'parents': [{'id': DRIVE_FOLDER_ID}]})
                file.SetContentFile(pdf_path)
                file.Upload()
                print(f"Saved and uploaded PDF for {document_number}")

                # Delete local PDF
                os.remove(pdf_path)

            except Exception as e:
                print(f"Error capturing tab {j+1} of record {document_number}: {e}")

        # Close tab and return to main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    except Exception as e:
        print(f"Error with document number {document_number}: {e}")

# === Done! Quit browser ===
driver.quit()
print("All Done!")
