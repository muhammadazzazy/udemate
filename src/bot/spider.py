"""Implement all common functionality between middleman bots."""
from abc import ABC, abstractmethod
from utils.logger import setup_logging


class Spider(ABC):
    """Implements constructor and abstract methods for all intermediary spiders."""

    def __init__(self, urls: set[str]) -> None:
        self.urls = urls
        self.logger = setup_logging()

    @abstractmethod
    def transform(self, url: str) -> str:
        """Return a Udemy link extracted from middleman link."""

    @abstractmethod
    def run(self) -> set[str]:
        """Return set of Udemy links extracted from middleman website."""
