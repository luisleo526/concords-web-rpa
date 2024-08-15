from typing import Union

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebBrowser:
    def __init__(self, ads_id=None, port=50360):
        if ads_id is None:
            self.driver = webdriver.Chrome()
            return

        self.ads_id = ads_id
        self.port = port
        resp = self.get_local_api_response()

        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])

        chrome_driver = resp["data"]["webdriver"]
        service = Service(executable_path=chrome_driver)
        self.driver = webdriver.Chrome(service=service, options=options)

    def maximize_window(self):
        try:
            self.driver.fullscreen_window()
        except:
            pass

        try:
            self.driver.maximize_window()
        except:
            pass

    def get_local_api_response(self):
        open_url = f"http://localhost:{self.port}/api/v1/browser/start?user_id={self.ads_id}&open_tabs=1"
        resp = requests.get(open_url).json()
        return resp

    def get_element(self, xpath, driver: Union[WebDriver, WebElement] = None):

        if driver is None:
            driver = self.driver

        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        return element

    def get_elements(self, xpath, driver: Union[WebDriver, WebElement] = None):

        if driver is None:
            driver = self.driver

        elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )

        return elements

    def click_button(self, xpath):
        button = self.get_element(xpath)
        button.click()

    def insert_text(self, xpath, text, clear=False):
        field = self.get_element(xpath)
        if clear:
            field.clear()
        field.send_keys(text)
