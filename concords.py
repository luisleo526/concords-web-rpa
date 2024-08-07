import time
from datetime import datetime, timedelta

import pytz
from selenium.webdriver.common.by import By

from browser import WebBrowser
from schemas import StockOrder, FutureOrder, TodayFutureOrder


class Concords(WebBrowser):
    FIRST_PAGE_BASE_XPATH = '/html/body/app-root/app-login2/div[1]/div[2]/div/div[2]/div[1]/div[1]/form/div[2]'
    ACCOUNT_FIELD_XPATH = '/html/body/app-root/app-login2/div[1]/div[2]/div/div[2]/div[1]/div[1]/form/div[2]/div[1]/div[1]/input'
    PASSWORD_FIELD_XPATH = FIRST_PAGE_BASE_XPATH + '/div[1]/div[2]/input'
    LOGIN_BUTTON_XPATH = FIRST_PAGE_BASE_XPATH + '/div[2]/input'

    ACCOUNT_PANEL_XPATH = '//*[@id="navbarTogglerDemo01"]/ul/li[3]/a'

    STOCK_MARKET_XPATH = '/html/body/app-root/app-main-frame/div[2]/app-bill-frame/div/aside/div/div[1]/div/label[1]'
    FUTURE_MARKET_XPATH = '/html/body/app-root/app-main-frame/div[2]/app-bill-frame/div/aside/div/div[1]/div/label[2]'

    TABLE_PATH = '//*[@id="agGrid"]/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div'

    def __init__(self, ads_id=None, port=50360):
        super().__init__(ads_id, port)
        self.driver.get("https://etradeweb.concords.com.tw/itrader/#/UserLogin")
        time.sleep(5)

    def login(self, account, password):
        self.inset_text(Concords.ACCOUNT_FIELD_XPATH, account)
        self.inset_text(Concords.PASSWORD_FIELD_XPATH, password)
        self.click_button(Concords.LOGIN_BUTTON_XPATH)
        time.sleep(5)
        self.click_button(Concords.ACCOUNT_PANEL_XPATH)

    def enter_stock_market(self):
        self.click_button(Concords.STOCK_MARKET_XPATH)

    def enter_future_market(self):
        self.click_button(Concords.FUTURE_MARKET_XPATH)

    def get_entries(self):
        table = self.get_element(Concords.TABLE_PATH)
        entries = table.find_elements(By.XPATH, './div')
        return entries

    def get_history_stock_orders(self, days=3) -> list[StockOrder]:
        history_orders_path = '/html/body/app-root/app-main-frame/div[2]/app-bill-frame/div/aside/div/div[2]/ul/li/ul/li[2]/a'
        self.click_button(history_orders_path)

        # Asia/Taipei, three days ago
        time_str = (datetime.now(pytz.timezone('Asia/Taipei')) - timedelta(days=days)).strftime('%Y-%m-%d')

        self.inset_text('//*[@id="main"]/form[2]/div[1]/input', time_str, clear=True)

        search_btn_xpath = '//*[@id="main"]/form[1]/div[3]/div[2]/button'
        self.click_button(search_btn_xpath)

        time.sleep(5)

        table_xpath = '//*[@id="agGrid"]/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div'
        table = self.get_element(table_xpath)
        orders = table.find_elements(By.XPATH, 'div')

        print(f'過去歷史{days}天的證券委託數量:', len(orders))

        objects = []
        for order in orders:
            cells = [cell.text for cell in order.find_elements(By.XPATH, 'div')]
            objects.append(StockOrder.from_list_data(cells))

        return objects

    def get_history_future_orders(self, days=3) -> list[FutureOrder]:
        history_orders_xpath = '/html/body/app-root/app-main-frame/div[2]/app-bill-frame/div/aside/div/div[2]/ul/li/ul/li[2]/a'
        self.click_button(history_orders_xpath)

        # Asia/Taipei, three days ago
        time_str = (datetime.now(pytz.timezone('Asia/Taipei')) - timedelta(days=days)).strftime('%Y-%m-%d')

        self.inset_text('//*[@id="main"]/form[2]/div[1]/input', time_str, clear=True)

        search_btn_xpath = '//*[@id="main"]/form[1]/div[4]/button'
        self.click_button(search_btn_xpath)

        time.sleep(5)

        table_xpath = '//*[@id="agGrid"]/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div'
        table = self.get_element(table_xpath)
        orders = table.find_elements(By.XPATH, 'div')

        print(f'過去歷史{days}天的期貨委託數量:', len(orders))

        objects = []
        for order in orders:
            cells = [cell.text for cell in order.find_elements(By.XPATH, 'div')]
            objects.append(FutureOrder.from_list_data(cells))

        return objects

    def get_today_future_orders(self) -> list[TodayFutureOrder]:
        today_future_orders_xpath = '/html/body/app-root/app-main-frame/div[2]/app-bill-frame/div/aside/div/div[2]/ul/li/ul/li[1]/a'
        self.click_button(today_future_orders_xpath)

        time.sleep(5)

        table_xpath = '//*[@id="agGrid"]/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div'
        table = self.get_element(table_xpath)
        orders = table.find_elements(By.XPATH, 'div')

        print(f'今日期貨委託數量:', len(orders))

        objects = []
        for order in orders:
            cells = [cell.text for cell in order.find_elements(By.XPATH, 'div')][1:]
            objects.append(TodayFutureOrder.from_list_data(cells))

        return objects
