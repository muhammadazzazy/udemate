"""Manage Selenium WebDriver for scraping links and automating course enrollment."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config import Config


def setup_brave(headless: bool):
    """Return Selenium WebDriver for Brave Browser."""
    config: Config = Config()
    options = Options()
    options.add_experimental_option(
        'debuggerAddress',
        f'127.0.0.1:{config.port_number}')
    options.binary_location = '/usr/bin/brave-browser'
    if headless:
        options.headless = True
    else:
        options.add_argument(f'--user-data-dir={config.user_data_dir}')
    driver = webdriver.Chrome(options=options)
    return driver
