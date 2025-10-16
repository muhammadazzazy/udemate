"""Manage browser used for scraping links and automating course enrollment."""
import platform
from pathlib import Path

import undetected_chromedriver as uc

from utils.config import Config
from utils.logger import setup_logging


class Browser:
    """Manage browser configuration and expose Undetected Chromedriver."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = setup_logging()

    def get_brave_path(self) -> str | None:
        """Return Brave Browser executable path based on the operating system."""
        paths: dict[str, str] = {
            'Windows': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
            'Linux': '/usr/bin/brave-browser',
            'Darwin': '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        }
        system: str = platform.system()
        brave_path: str | None = paths.get(system)
        return brave_path

    def setup(self, headless: bool) -> uc.Chrome:
        """
        Return Undetected Chromedriver for Brave Browser either in headless mode for scraping
        or with debugger address when automating course enrollment.
        """
        options = uc.ChromeOptions()
        brave_path: str | None = self.get_brave_path()
        if not brave_path:
            self.logger.critical(
                'Brave Browser executable not found. Exiting...'
            )
            raise FileNotFoundError('Brave Browser executable not found.')
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
        if not headless:
            return uc.Chrome(
                options=options,
                browser_executable_path=brave_path,
                user_data_dir=self.config.BROWSER_USER_DATA_DIR,
                headless=headless
            )
        return uc.Chrome(
            options=options,
            browser_executable_path=brave_path,
            headless=headless
        )
