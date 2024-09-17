import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from datetime import datetime

url = "https://www.google.com/finance/"


def pytest_addoption(parser):
    parser.addoption(
        "--local",
        action="store_true",
        default=False,
        help="Run tests locally"
    )
    parser.addoption(
        "--firefox",
        action="store_true",
        help="Switch browser from default Chrome to Firefox"
    )


@pytest.fixture(scope='function')
def driver(request):
    if request.config.getoption('--firefox'):
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()

    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    timestamp = datetime.now().strftime('%H-%M-%S')
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        feature_request = item.funcargs['request']
        driver = feature_request.getfixturevalue('driver')
        xfail = hasattr(report, 'wasxfail')
        screenshot_dir = os.path.join(os.getcwd(), 'screenshots')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        if (report.skipped and xfail) or (report.failed and not xfail):
            screenshot_path = os.path.join(screenshot_dir, f'{timestamp}.png')
            driver.save_screenshot(screenshot_path)
            extra.append(pytest_html.extras.image(screenshot_path))
            extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
            print(f"Test failed. Screenshot saved at {screenshot_path}")
        report.extra = extra
