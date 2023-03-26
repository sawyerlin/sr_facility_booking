import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIME_OUT = 20

def get_clickable(driver, by: By, search: str):
    return WebDriverWait(driver, TIME_OUT).until(
        EC.element_to_be_clickable((by, search)))

def get_locate(driver, by: By, search: str, timeout: float = TIME_OUT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, search))
    )

def wait_until_to_be_url(driver, url: str):
    WebDriverWait(driver, TIME_OUT).until(EC.url_to_be(url))

def wait_until_invisibility(driver, by: By, search: str, timeout: float = TIME_OUT):
    WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((by, search)))

def click_element(driver, by: By, search: str):
    retry_times = 0
    while retry_times < 3:
        try:
            get_clickable(driver, by, search).click()
            break
        except Exception: 
            retry_times += 1
            time.sleep(1)
            
