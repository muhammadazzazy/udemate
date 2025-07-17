"""Fetch Udemy links with coupons from iDC."""
import requests
from requests.exceptions import RequestException

from selenium.common.exceptions import TimeoutException, WebDriverException
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

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from iDC."""
        self.logger.info('iDC spider starting...')
        self.logger.info('Processing %d links from iDC...',
                         len(self.urls))
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                clean_url: str = url
                if url.count('/') > 4:
                    clean_url = self.clean(url)
                udemy_url: str = self.transform(clean_url)
                self.logger.info('%s ==> %s', clean_url, udemy_url)
                if udemy_url:
                    udemy_urls.add(udemy_url)
            except TimeoutException as e:
                self.logger.error('Timeout while parsing %s: %r', url, e)
                continue
            except WebDriverException as e:
                self.logger.error('Webdriver error for %s: %r', url, e)
                continue
            except RequestException as e:
                self.logger.error('HTTP request failed for %s: %r', url, e)
                continue
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('Read timeout error for %s: %r', url, e)
                continue
        self.logger.info('iDC spider scraped %d Udemy links.', len(udemy_urls))
        return udemy_urls
