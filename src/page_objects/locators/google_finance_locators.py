from selenium.webdriver.common.by import By


class GoogleFinanceLocators(object):
    header = (By.XPATH, "//a[@id='sdgBod']//span[@class='gb_sd gb_ad']")
    all_stock_symbols = (By.XPATH, "//ul[@class='sbnBtf']//child::div[@class='COaKTb']")