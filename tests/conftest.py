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
    chrome_options.add_argument('--remote-debugging-port=9222')  # Important!
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

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
