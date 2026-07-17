from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
import schedule
from datetime import datetime

from config import DOWNLOAD_FOLDER, NSE_URL
from telegram_helper import send_message, send_file


# ==========================
# CHROME SETUP
# ==========================

def setup_chrome():

    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    prefs = {
        "download.default_directory": DOWNLOAD_FOLDER,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


# ==========================
# MAIN JOB
# ==========================

def job():

    print("===================================")
    print("Job Started...")
    print("===================================")

    driver = setup_chrome()

    try:

        # Open NSE Website
        driver.get(NSE_URL)

        print("Page Title:", driver.title)

        wait = WebDriverWait(driver, 30)

        time.sleep(8)

        # ==========================
        # STOCK FUTURES SELECTION
        # ==========================
        print("Selecting Stock Futures...")

        category = Select(
            wait.until(
                EC.presence_of_element_located(
                    (By.ID, "sel-Pre-Open-Market")
                )
            )
        )

        category.select_by_value("FUTSTK")

        print("Stock Futures Selected")

        time.sleep(5)
        
        # ==========================
        # DOWNLOAD CSV
        # ==========================

        print("Waiting for Download button...")

        download_button = wait.until(
            EC.element_to_be_clickable(
                (By.PARTIAL_LINK_TEXT, "Download")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            download_button
        )

        time.sleep(2)

        try:
            download_button.click()
            print("Normal Click Success")

        except Exception:

            print("Normal Click Failed")
            print("Trying JavaScript Click...")

            driver.execute_script(
                "arguments[0].click();",
                download_button
            )

            print("JavaScript Click Success")

        print("Waiting for CSV Download...")

        downloaded = False

        for i in range(30):

            csv_files = [
                f for f in os.listdir(DOWNLOAD_FOLDER)
                if f.endswith(".csv")
            ]

            if csv_files:
                downloaded = True
                print("CSV Downloaded Successfully!")
                break

            time.sleep(1)

        if not downloaded:
            raise Exception("CSV Download Failed!")

        # ==========================
        # TELEGRAM MESSAGE
        # ==========================

        today = datetime.now().strftime("%Y-%m-%d")

        send_message(
            f"📊 NSE PRE OPEN\n\n"
            f"✅ CSV Download Completed\n"
            f"📅 Date: {today}"
        )

        latest_file = max(
            [
                os.path.join(DOWNLOAD_FOLDER, f)
                for f in os.listdir(DOWNLOAD_FOLDER)
                if f.endswith(".csv")
            ],
            key=os.path.getctime
        )

        send_file(latest_file)

        print("Telegram Message Sent")
        print("CSV Sent To Telegram")

    except Exception as e:

        print("Error:", e)

        send_message(
            f"❌ NSE Automation Failed\n\nError:\n{e}"
        )

    finally:

        driver.quit()

        print("Browser Closed")
        print("===================================")


# ==========================
# SCHEDULER
# ==========================

schedule.every().day.at("14:42").do(job)

print("===================================")
print("Automation Running...")
print("Waiting for 14:35 PM")
print("===================================")

while True:
    schedule.run_pending()
    time.sleep(1)