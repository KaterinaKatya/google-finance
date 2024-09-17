import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url = "https://www.google.com/finance/"


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        required=True,
    )
    parser.addoption(
        "--local",
        action="store_true",
        default=False,
        help="local tests being run"
    )
    parser.addoption(
        "--firefox",
        action="store",
        help="changing browser from default chrome to firefox"
    )


@pytest.fixture(scope='function')
def driver(request, url):
    # Determine the browser based on the environment variable or default to Chrome
    browser = os.environ.get('BROWSER', 'chrome')

    if browser == 'chrome':
        driver = webdriver.Chrome()
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Maximize window, delete cookies, and navigate to the URL
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)

    # Wait for login button (or other elements)
    wait = 10
    try:
        login_btn = WebDriverWait(driver, wait).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()=" Log In "]'))
        )
        print("Login button found")
    except TimeoutException:
        print("No login button within timeout")

    # Yield the driver for use in tests
    yield driver

    # Quit the driver after test execution
    driver.quit()
