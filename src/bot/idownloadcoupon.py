"""Fetch Udemy links with coupons from iDC."""
import requests
from requests.exceptions import RequestException

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import ReadTimeoutError

from bot.spider import Spider


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from iDC."""

    def scrape(self, url: str) -> str:
        """Scrape Udemy link from iDC link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 30)
        form = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'form.cart')))
        action_url = form.get_attribute('action')
        response = requests.get(action_url, allow_redirects=True, timeout=30)
        udemy_url: str = response.url
        return udemy_url

    def transform(self, url: str) -> str:
        """Convert iDC link to final Udemy link with coupon."""
        response = requests.get(url, allow_redirects=True, timeout=30)
        if 'idownloadcoupon' in response.url:
            udemy_url: str = self.scrape(url)
            return udemy_url
        return response.url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from iDC."""
        self.logger.info('iDC spider starting...')
        self.logger.info('Processing %d links from iDC...',
                         len(self.urls))
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                udemy_urls.add(udemy_url)
            except TimeoutException as e:
                self.logger.error('Timeout while parsing %s: %s', url, e)
                continue
            except WebDriverException as e:
                self.logger.error('WebDriver error for %s: %s', url, e)
                continue
            except RequestException as e:
                self.logger.error('HTTP request failed for %s: %s', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('ReadTimeoutError error for %s: %s', url, e)
                continue
        self.logger.info('iDC spider scraped %d Udemy links.', len(udemy_urls))
        return udemy_urls
