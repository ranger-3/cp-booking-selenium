from unittest.mock import MagicMock

import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from cp.pages.search_page import SearchPage
from cp.pages.service_page import ServicePage


@pytest.fixture
def faker() -> Faker:
    return Faker()


def create_chrome_driver():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver():
    driver = create_chrome_driver()
    yield driver
    driver.quit()


@pytest.fixture
def search_page(driver):
    page = SearchPage(driver)
    fake_element = MagicMock()
    fake_element.get_attribute.return_value = ""
    fake_wait = MagicMock()
    fake_wait.until.return_value = fake_element
    page.wait = fake_wait
    return page


@pytest.fixture
def service_page(driver):
    page = ServicePage(driver)
    fake_element = MagicMock()
    fake_wait = MagicMock()
    fake_wait.until.return_value = fake_element
    page.wait = fake_wait
    return page
