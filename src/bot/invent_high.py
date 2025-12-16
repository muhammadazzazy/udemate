"""Scrape Udemy links with coupons from Invent High."""
import requests
from bs4 import BeautifulSoup
from gotify import Gotify
from requests.exceptions import RequestException

from bot.spider import Spider
from config.bot import SpiderConfig


class InventHigh(Spider):
    """Get Udemy links with coupons from Invent High."""

    def __init__(self, *, config: SpiderConfig, gotify: Gotify, urls: list[str]) -> None:
        self.session = requests.Session()
        super().__init__(config=config, gotify=gotify, urls=urls)

    def transform(self, url: str) -> str | None:
        """Return Udemy link from Invent High link."""
        for attempt in range(self.config.retries):
            try:
                response: requests.Response = self.session.get(
                    url, timeout=self.config.timeout)
                html: str = response.text
                soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
                button = soup.select_one('a#couponval')
                href: str | None = button.get('href') if button else None
                if not href:
                    continue
                udemy_url: str = self.clean(href)
                self.logger.info('%s ==> %s', url, udemy_url)
                return udemy_url
            except RequestException as e:
                self.logger.error(
                    'Attempt %d: Error fetching %s: %s', attempt+1, url, str(e)
                )
                continue
        return None
