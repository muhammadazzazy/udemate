"""Encapsulate common attributes and functionality between middleman spiders."""
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import ParseResult, urlparse, parse_qs, urlencode, urlunparse

from gotify import Gotify

from utils.config import SpiderConfig
from utils.logger import setup_logging


class Spider(ABC):
    """Encapsulates shared attributes and abstract methods for intermediary scrapers."""

    def __init__(self, *, config: SpiderConfig, gotify: Gotify, urls: list[str]) -> None:
        self.config = config
        self.gotify = gotify
        self.urls = urls
        self.name = self.__class__.__name__
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

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from middleman website."""
        self.logger.info('Processing %d intermediary links from %s...',
                         len(self.urls), self.name)
        self.gotify.create_message(
            title=f'{self.name} spider started',
            message=f'Processing {len(self.urls)} intermediary links from {self.name}.'
        )
        udemy_urls: list[str] = []
        with ThreadPoolExecutor(max_workers=self.config.threads) as executor:
            futures = {executor.submit(
                self.transform, url): url for url in self.urls}
            for future in as_completed(futures):
                result: str | None = future.result()
                if result:
                    udemy_urls.append(result)
        self.logger.info('%s spider scraped %d Udemy links.',
                         self.name, len(udemy_urls))
        self.gotify.create_message(
            title=f'{self.name} spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from {self.name}.'
        )
        return sorted(set(udemy_urls))

    @abstractmethod
    def transform(self, url: str) -> str | None:
        """Return a Udemy link extracted from middleman link."""
