"""Manage browser used for scraping links and automating course enrollment."""
import platform
import shutil

import undetected_chromedriver as uc

from utils.config import Config
from utils.logger import setup_logging


class Browser:
    """Manage browser configuration and expose Undetected Chromedriver."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = setup_logging()

    def switch_tab(self, driver: uc.Chrome) -> None:
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

    def setup(self, headless: bool) -> uc.Chrome:
        """
        Return Undetected Chromedriver for Brave Browser either in headless mode for scraping
        or with debugger address when automating course enrollment.
        """
        options = uc.ChromeOptions()
        if platform.system() == 'Windows':
            brave_path: str = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        else:
            brave_path: str = shutil.which('brave-browser')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        driver = uc.Chrome(
            options=options,
            browser_executable_path=brave_path,
            user_data_dir=self.config.BROWSER_USER_DATA_DIR,
            headless=headless
        )
        self.switch_tab(driver)
        return driver
