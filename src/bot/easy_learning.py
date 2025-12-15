"""Scrape Udemy links with coupons from Easy Learning."""
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from bot.spider import Spider


class EasyLearning(Spider):
    """Get Udemy links with coupons from Easy Learning."""

    def transform(self, url: str) -> str | None:
        """Return Udemy link from Easy Learning link."""
        for i in range(self.retries):
            try:
                response: requests.Response = requests.get(
                    url, timeout=self.timeout)
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
                    'Attempt %d: Error fetching %s: %s', i+1, url, str(e)
                )
                continue
        return None

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from Easy Learning."""
        self.logger.info('Processing %d intermediary links from Easy Learning...',
                         len(self.urls))
        self.gotify.create_message(
            title='Easy Learning spider started',
            message=f'Processing {len(self.urls)} intermediary links from Easy Learning.'
        )
        udemy_urls: list[str] = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(
                self.transform, url): url for url in self.urls}
            for future in as_completed(futures):
                result: str | None = future.result()
                if result:
                    udemy_urls.append(result)

        self.logger.info('Easy Learning spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.gotify.create_message(
            title='Easy Learning spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from Easy Learning.'
        )
        return sorted(set(udemy_urls))
