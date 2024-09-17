from selenium.webdriver.common.by import By


class GoogleFinanceLocators(object):
    header = (By.XPATH, "//a[@title='Finance' and @id='sdgBod']")
    all_stock_symbols = (By.XPATH, "//ul[@class='sbnBtf']//child::div[@class='COaKTb']")