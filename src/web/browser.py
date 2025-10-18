"""Manage browser used for scraping links and automating course enrollment."""
import platform
import shutil
from pathlib import Path

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
        paths: dict[str, str] = {
            'Windows': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
            'Linux': shutil.which('brave-browser'),
            'Darwin': shutil.which('Brave Browser')
        }
        system: str = platform.system()
        self.logger.info('Detected OS: %s', system)
        brave_path: str | None = paths.get(system)
        if brave_path and Path(brave_path).exists():
            return brave_path
        message: str = 'Brave executable not found'
        self.logger.error(message)
        raise FileNotFoundError(message)

    def setup(self, headless: bool) -> uc.Chrome:
        """
        Return Undetected Chromedriver for Brave Browser either in headless mode for scraping
        or with debugger address when automating course enrollment.
        """
        options = uc.ChromeOptions()
        brave_path: str = self.get_brave_path()
        common_args: list[str] = [
            '--disable-extensions',
            '--disable-component-extensions-with-background-pages',
            '--process-per-site',
            '--disable-background-networking',
            '--disable-backgrounding-occluded-windows',
            '--aggressive-cache-discard',
            '--disable-renderer-backgrounding',
            '--renderer-process-limit=4',
            # '--disable-site-isolation-trials',
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
