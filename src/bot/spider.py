"""Encapsulate common attributes and functionality between middleman spiders."""
import re
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
        match = re.search(r'couponCode=([^&]+)', udemy_url)
        question_mark_idx: int = udemy_url.find('?')
        if match:
            coupon_code = match.group(1)
            if question_mark_idx != -1:
                udemy_url = udemy_url[:udemy_url.find(
                    '?')+1] + 'couponCode=' + coupon_code
                return udemy_url
        return udemy_url[:question_mark_idx] if question_mark_idx != -1 else udemy_url

    @abstractmethod
    def transform(self, url: str) -> str | None:
        """Return a Udemy link extracted from middleman link."""

    @abstractmethod
    def run(self) -> list[str]:
        """Return list of Udemy links extracted from middleman website."""
