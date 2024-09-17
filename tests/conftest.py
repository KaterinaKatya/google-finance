import pytest
from selenium import webdriver
import os
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.google.com/finance/"


@pytest.fixture(scope='function')
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument('--remote-debugging-pipe')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    # Common setup
    driver.maximize_window()
    driver.delete_all_cookies()

    yield driver

    driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--firefox",
        action="store_true",
        help="Run tests using Firefox"
    )

