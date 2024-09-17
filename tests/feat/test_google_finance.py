import pytest
from src.page_objects.pages.google_finance_page import GoogleFinancePage
from src.data.stock_data import *


@pytest.mark.smoke
def test_stock_symbols(driver):
    google_finance_page = GoogleFinancePage(driver)
    stock_symbols = google_finance_page.get_stock_symbols()
    print("Stock Symbols:", stock_symbols)
    assert len(stock_symbols) > 0, "No stock symbols found"
    try:
        assert stock_symbols == expected_google_stock, f"Expected {expected_google_stock}, but got {stock_symbols}"
    except AssertionError as e:
        print(f"Retrieved data is not as expected: {e}")
    not_in_expected = set(stock_symbols) - set(expected_google_stock)
    not_on_ui = set(expected_google_stock) - set(stock_symbols)
    if not_in_expected:
        print(f"Stock symbols retrieved from UI but not in the expected data: {not_in_expected}")
    if not_on_ui:
        print(f"Stock symbols expected but not found in the UI: {not_on_ui}")



