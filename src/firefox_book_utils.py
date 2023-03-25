import logging
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_utils import click_element, get_locate, get_clickable, wait_until_to_be_url
from utils import short_wait, long_wait

FACILITIES={
    'tennis':'2645cdd3-bbbe-11ec-befc-02447a44a47c'
}

BASE_URL = "https://app.iplusliving.com"

def _get_options(headless: bool = True)->Options:
    options = webdriver.FirefoxOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--no-sandbox')
    if headless:
        options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.set_preference("xpinstall.signatures.required", False)
    # options.set_preference("browser.formfill.enable", False)
    options.set_preference("signon.autofillForms", False)
    return options

def get_driver(headless: bool = True)->WebDriver:
    options = _get_options(headless=headless)
    driver = webdriver.Firefox(options=options)
    driver.install_addon("buster-firefox.xpi")
    return driver

def login(driver, username, password, site_url):
    driver.get(f"{site_url}site/login")
    username_field = get_clickable(driver, By.ID, "user-username")
    password_field = get_clickable(driver, By.ID, "user-password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    wait_until_to_be_url(driver, site_url)
    logging.info('login')

def go_to_facility(driver, facility, site_url):
    driver.get(f"{site_url}amenity/amenitybooking?amenity={FACILITIES[facility]}")
    logging.info('facility booking page')

def book(driver, date_slot, time_slot):
    click_element(driver, By.XPATH, f"//td[@data-date='{date_slot}' and contains(@class, 'fc-day-number')]")
    logging.info(f'clicked on date {date_slot}')

    datetime_slot = f"{date_slot} {time_slot}"
    click_element(driver, By.XPATH, f"//div[@data-link-start='{datetime_slot}']")
    logging.info(f'clicked on time {time_slot}')

    click_element(driver, By.XPATH, "//input[@name='submit-button']")
    logging.info('submit the choices')

def confirm_book(driver):
    checkbox = get_locate(driver, By.XPATH, "//input[@id='dynamicmodel-termsandconditions']")
    driver.execute_script("arguments[0].checked = true;", checkbox)
    logging.info('condition checkbox checked')

    click_element(driver, By.XPATH, "//input[@name='submit-button']")
    logging.info('clicked button on the booking')

    short_wait()

    click_element(driver, By.XPATH, "//button[contains(@class, 'confirm-ok')]")
    logging.info('clicked button on the booking confirmation')

    success_msg = get_locate(driver, By.XPATH, "//div[@class='success-msg']//p")
    logging.info(success_msg.text)