"""Manage browser used for scraping links and automating course enrollment."""
import os
import shutil
import platform
from abc import ABC, abstractmethod

import undetected_chromedriver as uc

from utils.logger import Logger


class Browser(ABC):
    """Manage browser configuration and expose Undetected Chromedriver."""

    def __init__(self, *, user_data_dir: str, major_version: int, logger: Logger) -> None:
        self.major_version = major_version
        self.user_data_dir = user_data_dir
        self.logger = logger

    @abstractmethod
    def get_executable_path(self) -> str:
        """Return browser executable path based on the operating system."""

    def delete_user_data_dir(self) -> None:
        """Delete user data directory to reset browser state."""
        if os.path.exists(self.user_data_dir):
            shutil.rmtree(self.user_data_dir)
            self.logger.info('Deleted user data directory: %s',
                             self.user_data_dir)

    def setup(self, headless: bool) -> uc.Chrome:
        """
        Return Undetected Chromedriver for a Chromium browser either in headless mode for scraping
        or in non-headless mode for automating course enrollment.
        """
        options = uc.ChromeOptions()
        browser_executable: str = self.get_executable_path()

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
        gui_args: list[str] = []
        if platform.system() == 'Windows':
            gui_args = [
                '--use-angle=d3d11'
            ]
        for arg in common_args + (headless_args if headless else gui_args):
            options.add_argument(arg)
        if not headless:
            self.delete_user_data_dir()
            return uc.Chrome(
                options=options,
                version_main=self.major_version,
                browser_executable_path=browser_executable,
                user_data_dir=self.user_data_dir,
                headless=headless
            )
        return uc.Chrome(
            options=options,
            version_main=self.major_version,
            browser_executable_path=browser_executable,
            headless=headless
        )
