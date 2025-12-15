"""Encapsulate the Course Treat spider methods and attributes."""
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from bot.spider import Spider


class CourseTreat(Spider):
    """Course Treat spider to get Udemy links with coupons."""

    def transform(self, url: str) -> str | None:
        """Return Udemy link from Course Treat link."""
        for i in range(self.retries):
            try:
                response: requests.Response = requests.get(
                    url, timeout=self.timeout)
                html: str = response.text
                soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
                btn = soup.select_one('a.btn-couponbtn')
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
        """Return list of Udemy links extracted from Course Treat."""
        self.logger.info('Processing %d links from Course Treat...',
                         len(self.urls))
        self.gotify.create_message(
            title='Course Treat spider started',
            message=f'Processing {len(self.urls)} intermediary links from Course Treat.'
        )
        udemy_urls: list[str] = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(
                self.transform, url): url for url in self.urls}
            for future in as_completed(futures):
                result: str | None = future.result()
                if result:
                    udemy_urls.append(result)
        self.logger.info('Course Treat spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.gotify.create_message(
            title='Course Treat spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from Course Treat.'
        )
        return sorted(set(udemy_urls))
