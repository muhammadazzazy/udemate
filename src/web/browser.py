"""Manage browser used for scraping links and automating course enrollment."""
from abc import ABC, abstractmethod

import undetected_chromedriver as uc

from utils.config import Config
from utils.logger import Logger


class Browser(ABC):
    """Manage browser configuration and expose Undetected Chromedriver."""

    def __init__(self, *, config: Config, logger: Logger) -> None:
        self.config = config
        self.logger = logger

    @abstractmethod
    def get_executable_path(self) -> str:
        """Return browser executable path based on the operating system."""

    def setup(self, headless: bool) -> uc.Chrome:
        """
        Return Undetected Chromedriver for a Chromium browser either in headless mode for scraping
        or in non-headless mode for automating course enrollment.
        """
        options = uc.ChromeOptions()
        brave_path: str = self.get_executable_path()
        common_args: list[str] = [
            '--disable-extensions',
            '--disable-component-extensions-with-background-pages',
            '--process-per-site',
            '--disable-background-networking',
            '--disable-backgrounding-occluded-windows',
            '--aggressive-cache-discard',
            '--disable-renderer-backgrounding',
            '--renderer-process-limit=4',
            '--disable-features=IsolateOrigins,site-per-process',
            '--blink-settings=imagesEnabled=false'
        ]
        headless_args: list[str] = [
            '--headless=new',
            '--disable-gpu',
            '--disable-software-rasterizer'
        ]
        gui_args: list[str] = [
            '--use-angle=d3d11'
        ]
        for arg in common_args + (headless_args if headless else gui_args):
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
