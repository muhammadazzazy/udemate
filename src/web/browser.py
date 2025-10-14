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

    def get_brave_path(self) -> str:
        """Return Brave Browser executable path based on the operating system."""
        if platform.system() == 'Windows':
            brave_path: str = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        else:
            brave_path: str = shutil.which('brave-browser')
        return brave_path

    def setup(self, headless: bool) -> uc.Chrome:
        """
        Return Undetected Chromedriver for Brave Browser either in headless mode for scraping
        or with debugger address when automating course enrollment.
        """
        options = uc.ChromeOptions()
        brave_path: str | None = self.get_brave_path()
        common_args: list[str] = [
            '--disable-extensions',
            '--disable-background-networking',
            '--disable-renderer-backgrounding',
            '--renderer-process-limit=2',
            '--disable-site-isolation-trials',
            '--blink-settings=imagesEnabled=false'
        ]
        headless_args: list[str] = [
            '--headless=new',
            '--disable-gpu',
            '--disable-software-rasterizer'
        ]
        for arg in common_args + (headless_args if headless else []):
            options.add_argument(arg)
            self.logger.debug('Added Chrome option: %s', arg)
        driver: uc.Chrome = uc.Chrome(
            options=options,
            browser_executable_path=brave_path,
            user_data_dir=self.config.BROWSER_USER_DATA_DIR,
            headless=headless
        )
        return driver
