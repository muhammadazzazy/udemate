"""Fetch Udemy links with coupons from iDC."""
import requests

from requests.exceptions import RequestException
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from iDC."""

    def transform(self, url: str) -> str:
        """Convert iDC link to final Udemy link with coupon."""
        response = requests.get(url, allow_redirects=True, timeout=30)
        return response.url

    def clean(self, url: str) -> str:
        """Return cleaned iDC link."""
        parts: list[str] = url.split('/')
        while '' in parts:
            parts.remove('')
        clean_url: str = parts[0] + '//' + '/'.join(parts[1:4])
        return clean_url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from iDC."""
        self.logger.info('iDC spider starting...')
        self.logger.info('Processing %d links from iDC...',
                         len(self.urls))
        clean_urls: list[str] = []
        for url in self.urls:
            if url.count('/') > 4:
                clean_url: str = self.clean(url)
                clean_urls.append(clean_url)
            else:
                clean_urls.append(url)

        udemy_urls: list[str] = []
        for clean_url in clean_urls:
            try:
                udemy_url: str = self.transform(clean_url)
                self.logger.info('%s ==> %s', clean_url, udemy_url)
                if udemy_url:
                    udemy_urls.append(udemy_url)
            except RequestException as e:
                self.logger.error(
                    'HTTP request failed for %s: %r', clean_url, e)
                continue
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', clean_url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error(
                    'Read timeout error for %s: %r', clean_url, e)
                continue
        self.logger.info('iDC spider scraped %d Udemy links.', len(udemy_urls))
        return sorted(set(udemy_urls))
