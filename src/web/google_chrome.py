"""Contains a method for determining executable path of Google Chrome based on the platform."""
import platform
import shutil
from pathlib import Path

from web.browser import Browser


class GoogleChrome(Browser):
    """Encapsulates a method associated with fetching executable path of Google Chrome."""

    def get_executable_path(self):
        """Return executable path of Google Chrome."""
        paths: dict[str, str] = {
            'Windows': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'Linux': shutil.which('google-chrome'),
            'Darwin': shutil.which('google-chrome')
        }
        system: str = platform.system()
        self.logger.debug('Detected OS: %s', system)
        chrome_path: str | None = paths.get(system)
        if chrome_path and Path(chrome_path).exists():
            return chrome_path
        message: str = 'Google Chrome executable not found'
        self.logger.error(message)
        raise FileNotFoundError(message)
