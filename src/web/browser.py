"""Manage browser used for scraping links and automating course enrollment."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from utils.config import Config
from utils.logger import setup_logging


class Browser:
    """Manage browser configuration and expose Selenium WebDriver."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = setup_logging()

    def switch_tab(self, driver: WebDriver) -> None:
        """Switch to newtab if open; otherwise switch to last opened tab."""
        tabs = driver.window_handles
        target_url: str = 'chrome://newtab/'
        for tab in tabs:
            driver.switch_to.window(tab)
            current_url: str = driver.current_url
            if current_url == target_url:
                self.logger.info("Switched to Brave Browser's launch tab.")
                return
        self.logger.warning('Launch tab not found. Defaulting to last tab.')
        driver.switch_to.window(driver.window_handles[-1])

    def setup(self, headless: bool) -> WebDriver:
        """
        Return Selenium WebDriver for Brave Browser either in headless mode for scraping
        or with debugger address when automating course enrollment.
        """
        options = Options()
        options.binary_location = '/usr/bin/brave-browser'
        options.add_argument('--disable-gpu')
        if headless:
            options.add_argument('--no-sandbox')
            options.add_argument(
                f'user-agent={self.config.BROWSER_USER_AGENT}')
            options.add_argument('--headless=new')
            return webdriver.Chrome(options=options)
        options.add_experimental_option(
            'debuggerAddress', f'127.0.0.1:{self.config.PORT}')
        driver: WebDriver = webdriver.Chrome(options=options)
        self.switch_tab(driver)
        return driver
