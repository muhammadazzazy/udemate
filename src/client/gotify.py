""""Encapsulate Gotify client setup and configuration."""
from logging import Logger

from gotify import Gotify
from httpx import ConnectError, ConnectTimeout, ReadError


class GotifyClient:
    """Contains Gotify client attributes and methods."""

    def __init__(self, *, base_url: str, app_token: str, logger: Logger) -> None:
        self.base_url = base_url
        self.app_token = app_token
        self.logger = logger

    def setup(self) -> Gotify:
        """Return Gotify client."""
        gotify: Gotify = Gotify(
            base_url=self.base_url,
            app_token=self.app_token
        )
        return gotify

    def create_message(self, *, title: str, message: str) -> None:
        """Send a message using Gotify."""
        gotify: Gotify = self.setup()
        try:
            gotify.create_message(
                title=title,
                message=message
            )
        except ConnectError as e:
            self.logger.error('Failed to send Gotify message: %r', e)
        except ConnectTimeout as e:
            self.logger.error('Failed to send Gotify message: %r', e)
        except ReadError as e:
            self.logger.error('Failed to send Gotify message: %r', e)
