from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_clickable(driver, by: By, search: str):
    return WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((by, search)))


def get_locate(driver, by: By, search: str):
    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((by, search))
    )

def click_element(driver, by: By, search: str):
    get_clickable(driver, by, search).click()