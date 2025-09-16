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
                        "value": "00871F1882E0F2A10D4920523BE4A930A6DB03402CBD0C965837E7559FB1A409FBCCBAAF405118C66C7E0F633D77B2EE7ED4E0403FC0CBC40B9837E15F1D2CD350D2583E1BB4F2A73FA0520B47C592556050585FB28C78E2CAAD92F9F809E4C6E20478F0EF57F64F564EEF9011551159EE37E2ADFF17F24754EC0A667582179451C8C58D54D2C95C2D48C281FEDA1EC7576E07565CE1ED7928E31B1F892969A88660E4E51810A61841A1B16274FC89A8FECFD904DC467F68849590E5E61EC99544EF56C91A3D91F071391AD7880EF025737A8306C58C84A044D609757DCF6C3158D92C7582011834BFFEA2B2ABCB8E7285014E57B5653A703B8D90C7981447B27F99D3037110408126A07CC982A7B745BA1EABDA0203C2AB784517C4F7CA8CFD9551994886A3814F2425374547EDA81DDEB4CDCAA8AB6DA2DBD5B3BE73AB27C2DE1CD368EC95677760B40C5C4A97AA19776A7D115239466A981A5A88CD95E3744B0B3D99DC80A92EEFDB164DE79FC63832"})
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
