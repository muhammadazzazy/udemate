"""Scrape Udemy links with coupons from WebHelperApp."""
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from bot.spider import Spider


class WebHelperApp(Spider):
    """Get Udemy links with coupons from WebHelperApp."""

    def transform(self, url: str) -> str | None:
        """Return Udemy link from WebHelperApp link."""
        for i in range(self.retries):
            try:
                response: requests.Response = requests.get(
                    url, timeout=self.timeout)
                html: str = response.text
                soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
                button = soup.select_one(
                    'a.wp-block-button__link.has-vivid-cyan-blue-background-color.has-background.wp-element-button'
                )
                href: str | None = button.get('href') if button else None
                if not href:
                    continue
                udemy_url: str = self.clean(href)
                self.logger.info('%s ==> %s', url, udemy_url)
                return udemy_url
            except RequestException as e:
                self.logger.error(
                    'Attempt %d: Error fetching %s: %s', i+1, url, str(e)
                )
                continue
        return None

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from WebHelperApp."""
        self.logger.info('Processing %d links from WebHelperApp...',
                         len(self.urls))
        self.gotify.create_message(
            title='WebHelperApp spider started',
            message=f'Processing {len(self.urls)} intermediary links from WebHelperApp.'
        )
        udemy_urls: list[str] = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(
                self.transform, url): url for url in self.urls}
            for future in as_completed(futures):
                result: str | None = future.result()
                if result:
                    udemy_urls.append(result)
        self.logger.info('WebHelperApp spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.gotify.create_message(
            title='WebHelperApp spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from WebHelperApp.'
        )
        return sorted(set(udemy_urls))
