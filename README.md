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


