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
    print("Test executed successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    driver.quit()
    sys.exit(1)

try:
    result = driver.find_element_by_xpath("//a[contains(@href, 'aboutus')]")
    result.click()
    print("Test executed successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    driver.quit()
    sys.exit(1)

try:
    result = driver.find_element_by_xpath("//button[contains(@class, 'openbtn')]")
    result.click()
    print("Test executed successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    driver.quit()
    sys.exit(1)

try:
    result = driver.find_element_by_xpath("//a[contains(@href, 'contact')]")
    result.click()
    print("Test executed successfully")
except Exception as e:
    print("ERROR: test failed: {}".format(e))
    driver.quit()
    sys.exit(1)
