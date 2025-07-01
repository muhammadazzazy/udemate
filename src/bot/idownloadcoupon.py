"""Fetch Udemy links with coupons from IDC."""
import requests
from requests.exceptions import RequestException

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bot.spider import Spider


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from IDC."""

    def scrape(self, url: str) -> str:
        """Scrape Udemy link from IDC link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 30)
        form = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'form.cart')))
        action_url = form.get_attribute('action')
        response = requests.get(action_url, allow_redirects=True, timeout=10)
        udemy_url: str = response.url
        return udemy_url

    def transform(self, url: str) -> str:
        """Convert IDC link to final Udemy link with coupon."""
        response = requests.get(url, allow_redirects=True, timeout=10)
        if 'udemy.com' not in url:
            udemy_url: str = self.scrape(url)
            return udemy_url
        return response.url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from IDC."""
        self.logger.info('IDC bot starting...')
        self.logger.info('Processing %d links from IDC...',
                         len(self.urls))
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                udemy_urls.add(udemy_url)
            except (RequestException, WebDriverException):
                self.logger.info('Something went wrong. Skipping...')
                continue
        self.logger.info('IDC bot scraped %d Udemy links.', len(udemy_urls))
        return udemy_urls
