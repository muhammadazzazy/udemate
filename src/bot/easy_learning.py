"""Scrape Udemy links with coupons from Easy Learning."""
import requests
from bs4 import BeautifulSoup
from gotify import Gotify
from requests.exceptions import RequestException

from bot.spider import Spider
from utils.config import SpiderConfig


class EasyLearning(Spider):
    """Get Udemy links with coupons from Easy Learning."""

    def __init__(self, *, config: SpiderConfig, gotify: Gotify, urls: list[str]) -> None:
        self.session = requests.Session()
        super().__init__(gotify=gotify, config=config, urls=urls)

    def transform(self, url: str) -> str | None:
        """Return Udemy link from Easy Learning link."""
        for attempt in range(self.config.retries):
            try:
                response: requests.Response = self.session.get(
                    url, timeout=self.config.timeout)
                html: str = response.text
                soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
                btn = soup.select_one('a.purple-button')
                href: str = btn.get('href')
                if not href:
                    continue
                udemy_url: str | None = self.clean(href)
                self.logger.info('%s ==> %s', url, udemy_url)
                return udemy_url
            except RequestException as e:
                self.logger.error(
                    'Attempt %d: Error fetching %s: %s', attempt+1, url, str(e)
                )
                continue
        return None
