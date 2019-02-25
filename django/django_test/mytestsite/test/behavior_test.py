#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

driver = webdriver.Chrome()
try:
    driver.maximize_window()
except Exception as e:
    pass

driver.get("http://127.0.0.1:8000/")

try:
    result = driver.find_element_by_xpath("//button[contains(@class, 'openbtn')]")
    result.click()
    print("clicked openbtn successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    driver.quit()
    sys.exit(1)

try:
    result = driver.find_element_by_xpath("//a[contains(@href, 'aboutus')]")
    result.click()
    print("clicked aboutus successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    driver.quit()
    sys.exit(1)

try:
    result = driver.find_element_by_xpath("//button[contains(@class, 'openbtn')]")
    result.click()
    print("clicked openbtn successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    driver.quit()
    sys.exit(1)

try:
    result = driver.find_element_by_xpath("//a[contains(@href, 'contact')]")
    result.click()
    print("clicked contact successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    #driver.quit()
    #sys.exit(1)

#driver.quit()

# search_box = driver.find_element_by_name("q")
# search_box.send_keys("testing")
# search_box.send_keys(Keys.RETURN)
# assert "Search" in driver.title
# # Locate first result in page using css selectors.
# result = driver.find_element_by_css_selector("button#openbtn")
# result.click()
# assert "testing" in driver.title.lower()
# driver.quit()
