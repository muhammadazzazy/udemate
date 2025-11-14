""""Encapsulate Gotify client setup and configuration."""
from logging import Logger

from gotify import Gotify
from httpx import ReadError


class GotifyClient:
    """Encapsulate Gotify client setup and configuration."""

    def __init__(self, *, base_url: str, app_token: str, logger: Logger) -> None:
        self.base_url = base_url
        self.app_token = app_token
        self.logger = logger

    def setup(self) -> Gotify:
        """Return Gotify client."""
        gotify_client: Gotify = Gotify(
            base_url=self.base_url,
            app_token=self.app_token
        )
        return gotify_client

    def create_message(self, *, title: str, message: str) -> None:
        """Send a message using Gotify."""
        try:
            gotify: Gotify = self.setup()
            gotify.create_message(
                title=title,
                message=message
            )
        except ReadError as e:
            self.logger.error('Failed to send Gotify message: %r', e)
