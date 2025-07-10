# Script to inspect the computed width of the .container element in a real browser
# This script uses Selenium to open the test_real_css_container_width.html and print the width of the .container element
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1600,1000')

# Path to the test file
file_url = 'file://' + __import__('os').path.abspath('test_real_css_container_width.html')

with webdriver.Chrome(options=options) as driver:
    driver.get(file_url)
    time.sleep(1)  # Wait for rendering
    container = driver.find_element(By.CLASS_NAME, 'container')
    width = driver.execute_script('return arguments[0].offsetWidth;', container)
    print(f"[RESULT] .container offsetWidth: {width}px")
    style_width = driver.execute_script('return window.getComputedStyle(arguments[0]).width;', container)
    print(f"[RESULT] .container computed CSS width: {style_width}")
