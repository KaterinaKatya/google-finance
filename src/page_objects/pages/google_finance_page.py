from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.page_objects.locators.google_finance_locators import GoogleFinanceLocators

class GoogleFinancePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_stock_symbols(self):
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(GoogleFinanceLocators.all_stock_symbols)
            )
            return [element.text for element in elements]
        except TimeoutException:
            print("Failed to load stock symbols")
            return []