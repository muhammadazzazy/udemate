"""Implement all common functionality between middleman bots."""
from abc import ABC, abstractmethod

from utils.logger import setup_logging


class Bot(ABC):
    """Implements constructor and abstract methods for all bots."""

    def __init__(self, driver, urls) -> None:
        self.driver = driver
        self.urls = urls
        self.logger = setup_logging()

    @abstractmethod
    def scrape(self, url: str) -> str:
        """Return a Udemy link extracted from middleman website."""

    @abstractmethod
    def run(self) -> set[str]:
        """Return set of Udemy links extracted from middleman website."""
