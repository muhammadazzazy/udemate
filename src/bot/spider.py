"""Encapsulate common attributes and functionality between middleman spiders."""
from urllib.parse import ParseResult, urlparse, parse_qs, urlencode, urlunparse
from abc import ABC, abstractmethod

from gotify import Gotify

from utils.config import SpiderConfig
from utils.logger import setup_logging


class Spider(ABC):
    """Encapsulates shared attributes and abstract methods for intermediary scrapers."""

    def __init__(self, *, urls: list[str], gotify: Gotify, config: SpiderConfig) -> None:
        self.urls = urls
        self.gotify = gotify
        self.retries = config.retries
        self.timeout = config.timeout
        self.threads = config.threads
        self.logger = setup_logging()

    def clean(self, url: str) -> str:
        """Return clean Udemy link with coupon code."""
        parsed: ParseResult = urlparse(url)
        params: dict[str, list[str]] = parse_qs(parsed.query)
        udemy_url: str = params.get('u', [url])[0]
        udemy_parsed: ParseResult = urlparse(udemy_url)

        udemy_params: dict[str, list[str]] = parse_qs(udemy_parsed.query)

        clean_params: dict[str, list[str]] = {}
        if 'couponCode' in udemy_params:
            clean_params['couponCode'] = udemy_params['couponCode']

        clean_query: str = urlencode(clean_params, doseq=True)

        return urlunparse(
            udemy_parsed._replace(query=clean_query)
        )

    @abstractmethod
    def transform(self, url: str) -> str | None:
        """Return a Udemy link extracted from middleman link."""

    @abstractmethod
    def run(self) -> list[str]:
        """Return list of Udemy links extracted from middleman website."""
