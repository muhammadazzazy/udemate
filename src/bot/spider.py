"""Encapsulate common attributes and functionality between middleman spiders."""
import urllib.parse as urlparse
from abc import ABC, abstractmethod

from gotify import Gotify

from utils.config import BotConfig
from utils.logger import setup_logging


class Spider(ABC):
    """Encapsulates shared attributes and abstract methods for intermediary scrapers."""

    def __init__(self, *, urls: list[str], gotify: Gotify, config: BotConfig) -> None:
        self.urls = urls
        self.gotify = gotify
        self.retries = config.retries
        self.timeout = config.timeout
        self.threads = config.threads
        self.logger = setup_logging()

    def clean(self, url: str) -> str:
        """Return clean Udemy link without tracking parameters."""
        parsed = urlparse.urlparse(url)
        params = urlparse.parse_qs(parsed.query)
        udemy_url: str = params.get('u', [url])[0]
        i: int = udemy_url.find('&im_ref')
        if i != -1:
            return udemy_url[:i]
        j: int = udemy_url.find('?im_ref')
        if j != -1:
            return udemy_url[:j]
        return udemy_url

    @abstractmethod
    def transform(self, url: str) -> str | None:
        """Return a Udemy link extracted from middleman link."""

    @abstractmethod
    def run(self) -> list[str]:
        """Return list of Udemy links extracted from middleman website."""
