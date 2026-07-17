from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://www.nseindia.com/market-data/pre-open-market-fno")

time.sleep(10)

selects = driver.find_elements(By.TAG_NAME, "select")

print("Total select tags:", len(selects))

for i, s in enumerate(selects):
    print("=" * 50)
    print("Select", i + 1)
    print("ID:", s.get_attribute("id"))
    print("NAME:", s.get_attribute("name"))
    print("CLASS:", s.get_attribute("class"))
    print("HTML:")
    print(s.get_attribute("outerHTML"))

input("Press Enter...")
driver.quit()