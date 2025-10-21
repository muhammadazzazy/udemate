"""Implement all common functionality between middleman bots."""
from abc import ABC, abstractmethod
from utils.logger import setup_logging


class Spider(ABC):
    """Implements constructor and abstract methods for all intermediary spiders."""

    def __init__(self, urls: list[str]) -> None:
        self.urls = urls
        self.logger = setup_logging()

    def clean(self, url: str) -> str:
        """Return cleaned middleman link."""
        index: int = url.find('&im_ref=')
        if index != -1:
            return url[:index]
        return url

    @abstractmethod
    def transform(self, url: str) -> str:
        """Return a Udemy link extracted from middleman link."""

    @abstractmethod
    def run(self) -> list[str]:
        """Return list of Udemy links extracted from middleman website."""
