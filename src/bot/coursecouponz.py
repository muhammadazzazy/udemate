"""Scrape Udemy links with coupons from CourseCouponz."""
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

from bot.spider import Spider


class CourseCouponz(Spider):
    """Get Udemy links with coupons from CourseCouponz."""

    def transform(self, url: str) -> str | None:
        """Return Udemy link from CourseCouponz link."""
        for i in range(self.retries):
            try:
                response: requests.Response = requests.get(
                    url, timeout=self.timeout)
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
            except requests.RequestException as e:
                self.logger.error(
                    'Attempt %d: Error fetching %s: %s', i+1, url, str(e)
                )
                continue
        return None

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from CourseCouponz."""
        self.logger.info('Processing %d intermediary links from CourseCouponz...',
                         len(self.urls))
        self.gotify.create_message(
            title='CourseCouponz spider started',
            message=f'Processing {len(self.urls)} intermediary links from CourseCouponz.'
        )
        udemy_urls: list[str] = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(
                self.transform, url): url for url in self.urls}
            for future in as_completed(futures):
                result: str | None = future.result()
                if result:
                    udemy_urls.append(result)
        self.logger.info('CourseCouponz spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.gotify.create_message(
            title='CourseCouponz spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from CourseCouponz.'
        )
        return sorted(set(udemy_urls))
