"""Scrape Udemy links with coupons from Easy Learning."""
import requests
from bs4 import BeautifulSoup
from logging import Logger
from requests.exceptions import RequestException

from bot.spider import Spider
from config.bot import SpiderConfig


class EasyLearning(Spider):
    """Get Udemy links with coupons from Easy Learning."""

    def __init__(self, *, config: SpiderConfig, urls: list[str], logger: Logger) -> None:
        self.session = requests.Session()
        super().__init__(config=config, urls=urls, logger=logger)

    def transform(self, url: str) -> str | None:
        """Return Udemy link from Easy Learning link."""
        for attempt in range(self.config.retries):
            try:
                response: requests.Response = self.session.get(
                    url, timeout=self.config.timeout)
                html: str = response.text
                soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
                btn = soup.select_one('a.purple-button')
                if not btn:
                    continue
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
