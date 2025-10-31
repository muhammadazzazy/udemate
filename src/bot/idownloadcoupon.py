"""Fetch Udemy links with coupons from iDC."""
import requests
from requests.exceptions import RequestException

from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from iDC."""

    def __init__(self, *, urls: list[str], retries: int, timeout: int) -> None:
        self.session = requests.Session()
        super().__init__(urls=urls, retries=retries, timeout=timeout)

    def transform(self, url: str) -> str | None:
        """Convert iDC link to final Udemy link with coupon."""
        response: requests.Response = self.session.get(
            url, allow_redirects=True, timeout=self.timeout)
        url: str = self.clean(response.url)
        count: int = 0
        while 'udemy.com' not in url and count < self.retries:
            response = self.session.get(
                url, allow_redirects=True, timeout=self.timeout)
            url = self.clean(response.url)
            count += 1
        return url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from iDC."""
        self.logger.info('iDC spider starting...')
        self.logger.info('Processing %d links from iDC...',
                         len(self.urls))
        udemy_urls: list[str] = []
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                if udemy_url:
                    udemy_urls.append(udemy_url)
            except RequestException as e:
                self.logger.error(
                    'HTTP request failed for %s: %r', url, e)
                continue
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error(
                    'Read timeout error for %s: %r', url, e)
                continue
        self.logger.info('iDC spider scraped %d Udemy links.', len(udemy_urls))
        return sorted(set(udemy_urls))
