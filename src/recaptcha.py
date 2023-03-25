import logging
import numpy as np
import scipy.interpolate as si
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import short_wait, long_wait

def human_like_mouse_move(action, start_element):

    points = [[6, 2], [3, 2],[0, 0], [0, 2]];
    points = np.array(points)
    x = points[:,0]
    y = points[:,1]


    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)


    x_tup = si.splrep(t, x, k=1)
    y_tup = si.splrep(t, y, k=1)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    start_element_internal = start_element

    action.move_to_element(start_element_internal)
    action.perform()

    c = 5
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x,mouse_y)
        action.perform()
        print("Move mouse to, %s ,%s" % (mouse_x, mouse_y))   
        i += 1    
        if i == c:
            break

def solve_recaptcha(driver):

    driver.switch_to.default_content()
    logging.info("Switch to new frame")
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])

    logging.info("Wait for recaptcha-anchor")
    check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))

    logging.info("Wait")
    short_wait()

    action =  ActionChains(driver)
    human_like_mouse_move(action, check_box)

    logging.info("Click")
    check_box.click()

    logging.info("Wait")
    short_wait()

    logging.info("Mouse movements")
    action = ActionChains(driver)
    human_like_mouse_move(action, check_box)

    try:
        logging.info("Switch Frame")
        driver.switch_to.default_content()
        recaptcha_challenge_iframe = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'recaptcha challenge')]"))
        )
        if recaptcha_challenge_iframe:
            driver.switch_to.frame(recaptcha_challenge_iframe)
            short_wait()
            logging.info("Finding solver button")
            tab_act = ActionChains(driver)
            tab_act.send_keys(Keys.TAB).perform()
            short_wait()
            tab_act.send_keys(Keys.TAB).perform()
            short_wait()
            tab_act.send_keys(Keys.ENTER).perform()

            long_wait()

            driver.switch_to.default_content()
            logging.info("Switch to default")
    except Exception as ex:
        logging.info("no challenge", ex)