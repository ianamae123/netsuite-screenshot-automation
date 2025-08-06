# Netsuite Screenshot Automation Project

## Project Overview

This python script automates taking screenshots of individual Netsuite transaction records from a saved search and uploads them to a Google Drive folder with the document number as its name. It uses Selenium for browser automation, PyDrive for Google Drive API access, and PyAutoGUI for capturing screenshots.

## Tools and Technologies Used
- Python 3.9+
- Selenium WebDriver with ChromeDriver
- PyDrive (Google Drive API wrapper)
- PyAutoGUI (for screenshots)
- Google Cloud Console OAuth 2.0 for authenication


## Setup & Installation
- Install Python 3.9+
- Install required Python packages: 
```shell
pip install selenium pydrive pyautogui
```
- Download and place ChromeDriver in your system PATH
- Create Google OAuth in Google Cloud Console and download client_secrets.json into your project folder

## Key Features and Adjustability
- **Login Wait Time:** The script wait 20 seconds after opening the NetSuite page for manual login
- **Record Selection:** Uses CSS selectors to identify record links, which can be modified if needed
- **Screenshot Naming:** Automatically names screenshot as CR#<document_number>.png by extracting the document number from the record page

## How it works
1. It opens the saved search URL in a browser
2. Waits for manual login
3. Finds all record links on the page
4. Iterates over each record: 
    1. Opens a record in a new tab
    2. Extracts the document number
    3. Takes a screenshot
    4. Names the screen shot as CR#<document_number>.png
    5. Uploads to Google Drive
    6. Closes tab
    7. Repeat step 4a with a new record

## Issues
- Only shows one record at the bottom
- Only iterates through what is clickable on the first page, if there are records on anoother page, we would need to handle that
- Zoom out, check if it is at the end of page then takes a screenshot
    - if there are multiple tabs at the bottom, have it look through each

## In-Progress
- Click to other record pages if there is more than one page
- Open tabs on bottom and take a screenshot of each, and name accordingly

