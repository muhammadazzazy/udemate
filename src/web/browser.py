"""Manage browser used for scraping links and automating course enrollment."""
import getpass
import os
from typing import Final

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from utils.logger import setup_logging

DEFAULT_PORT: Final[int] = 9222
USER: Final[str] = getpass.getuser()
DEFAULT_USER_DATA_DIR: Final[str] = f'/home/{USER}/.config/BraveSoftware/Brave-Browser'
DEFAULT_PROFILE_DIR: Final[str] = 'Default'


class Browser:
    """Manage browser configuration and expose Selenium WebDriver."""

    def __init__(self) -> None:
        self.port = os.environ.get('PORT', DEFAULT_PORT).strip('"')
        self.user_data_dir = os.environ.get('USER_DATA_DIR',
                                            DEFAULT_USER_DATA_DIR).strip('"')
        self.profile_dir = os.environ.get('PROFILE_DIR',
                                          DEFAULT_PROFILE_DIR).strip('"')
        self.user_agent = os.environ.get('BROWSER_USER_AGENT', '').strip('"')
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
            options.add_argument(f'user-agent={self.user_agent}')
            options.add_argument('--headless=new')
            return webdriver.Chrome(options=options)
        options.add_experimental_option(
            'debuggerAddress', f'127.0.0.1:{self.port}')
        driver: WebDriver = webdriver.Chrome(options=options)
        self.switch_tab(driver)
        return driver
