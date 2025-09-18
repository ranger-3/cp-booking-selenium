from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def create_driver(
    headless: bool = True, window_size: str = "1280,900"
) -> webdriver.Chrome:
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={window_size}")

    driver = webdriver.Chrome(options=options)
    return driver
