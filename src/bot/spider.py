"""Encapsulate common attributes and functionality between middleman spiders."""
from abc import ABC, abstractmethod

from gotify import Gotify

from utils.logger import setup_logging


class Spider(ABC):
    """Encapsulates shared attributes and abstract methods for intermediary scrapers."""

    def __init__(self, *, urls: list[str], gotify: Gotify, retries: int, timeout: int) -> None:
        self.urls = urls
        self.gotify = gotify
        self.retries = retries
        self.timeout = timeout
        self.logger = setup_logging()

    def clean(self, url: str) -> str:
        """Return cleaned middleman link."""
        index: int = url.find('&im_ref=')
        if index == -1:
            index = url.find('/?im_ref=')

        if index != -1:
            return url[:index]
        return url

    @abstractmethod
    def transform(self, url: str) -> str:
        """Return a Udemy link extracted from middleman link."""

    @abstractmethod
    def run(self) -> list[str]:
        """Return list of Udemy links extracted from middleman website."""
