"""Manage browser used for scraping links and automating course enrollment."""
import getpass
import os
import subprocess
import time
from typing import Final

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


DEFAULT_PORT: Final[int] = 9222
USER: Final[str] = getpass.getuser()
DEFAULT_USER_DATA_DIR: Final[str] = f'/home/{USER}/.config/BraveSoftware/Brave-Browser'
DEFAULT_PROFILE_DIR: Final[str] = 'Default'


class Browser:
    """Manage browser configuration and expose Selenium WebDriver."""

    def __init__(self) -> None:
        self.port = os.environ.get('PORT', DEFAULT_PORT)
        self.user_data_dir = os.environ.get(
            'USER_DATA_DIR', DEFAULT_USER_DATA_DIR)
        self.profile_dir = os.environ.get('PROFILE_DIR', DEFAULT_PROFILE_DIR)

    def launch(self) -> None:
        """
        Launch Brave Browser for automating Udemy course enrollment.
        """
        subprocess.run([
            'brave-browser',
            f'--remote-debugging-port={self.port}',
            f'--user-data-dir={self.user_data_dir}',
            f'--profile-directory={self.profile_dir}',
        ], check=True)
        time.sleep(3)

    def setup(self, headless: bool):
        """
        Return Selenium WebDriver either in headless mode for scraping Udemy links 
        or in debugger address when automating course enrollment.
        """
        options = Options()
        if headless:
            options.add_argument('--headless')
        else:
            self.launch()
            options.add_experimental_option(
                'debuggerAddress', f'127.0.0.1:{self.port}')
        driver = webdriver.Chrome(options=options)
        return driver
