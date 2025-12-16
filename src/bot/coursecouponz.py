"""Scrape Udemy links with coupons from CourseCouponz."""
import requests
from bs4 import BeautifulSoup
from gotify import Gotify
from requests.exceptions import RequestException

from config.bot import BotConfig
from bot.spider import Spider


class CourseCouponz(Spider):
    """Get Udemy links with coupons from CourseCouponz."""

    def __init__(self, *, config: BotConfig, urls: list[str],
                 gotify: Gotify) -> None:
        self.session = requests.Session()
        super().__init__(urls=urls, config=config, gotify=gotify)

    def transform(self, url: str) -> str | None:
        """Return Udemy link from CourseCouponz link."""
        for attempt in range(self.config.retries):
            try:
                response: requests.Response = self.session.get(
                    url, timeout=self.config.timeout)
                html: str = response.text
                soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
                elements = soup.select(
                    'a.elementor-button.elementor-button-link.elementor-size-sm')
                btn = elements[-1] if elements else None
                href: str = btn.get('href')
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
