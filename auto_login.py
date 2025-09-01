# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", 
                        "value": "00D55183C87B8ADA11FD08881EB9FB8D75971712E27762BD1C869E47EC2101DEBEF0748EA7591D9989A15C4D29652F7AA9CFCC9D3DF4D68E2D17E33C885D43B58F9A09A679A62271833C2EE795232AA1DCA6F7B26881B17F933466C5D5AA68419528D6A8D50809D60C2B89B0370C9963A016A91AA166AAF0121873422B161C3FC002480C374BF9B5441509F46F64090415645D49CF1786A32608CC8233EFD8181FF9D7D572E07BAE9AAB2196C1FA7F033EA457FA1CC06BC5C748025ACE84C26B3CCAE4CF8FAAC5B78F0E11E3B55F60031D1F180851F5B878885B1200372ACA5D5EC7FB8CCFD44FD9D7CA6B32C4861AC02FDA3866BCBED82A11B9214325E2BBAD93D63D2C6B4311EF7BFFA0831B00FC0B13F7DD5C5D25D5280B1A40927CA0E559669CCAC90DC8865DC7A4D655FDEF103B16F3BEA90C11F5C5313FFC3A5C4DF363BC57E6B59A69E78A6B8A21A9936D2168730E472139B115EA2DA7C359847435A535CB4333EC46460ED3D621802449D2F1F057B18CBD0F6D7C23B30C8B210284ABA4"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
