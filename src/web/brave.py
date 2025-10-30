"""Contains a method for determining executable path of Brave Browser based on the platform."""
import platform
import shutil
from pathlib import Path


from web.browser import Browser


class Brave(Browser):
    """Encapsulates a method associated with fetching executable path of Brave Browser."""

    def get_executable_path(self) -> str:
        """Return executable path of Brave Browser."""
        paths: dict[str, str] = {
            'Windows': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
            'Linux': shutil.which('brave-browser'),
            'Darwin': shutil.which('Brave Browser')
        }
        system: str = platform.system()
        self.logger.debug('Detected OS: %s', system)
        brave_path: str | None = paths.get(system)
        if brave_path and Path(brave_path).exists():
            return brave_path
        message: str = 'Brave executable not found'
        self.logger.error(message)
        raise FileNotFoundError(message)
