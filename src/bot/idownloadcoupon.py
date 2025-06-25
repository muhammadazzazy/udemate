"""Fetch Udemy links with coupons from IDC."""
import requests
from requests.exceptions import RequestException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from utils.logger import setup_logging


class IDownloadCoupon:
    """Get Udemy links with coupons from IDC."""

    def __init__(self, driver: WebDriver, urls: set[str]) -> None:
        self.driver = driver
        self.urls = urls
        self.logger = setup_logging()

    def scrape(self, url: str) -> str:
        """Scrape Udemy link from IDC link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 15)
        form = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "form.cart")))
        action_url = form.get_attribute("action")
        response = requests.get(action_url, allow_redirects=True, timeout=15)
        udemy_url: str = response.url
        self.logger.info('%s ===> %s', url, udemy_url)
        return udemy_url

    def transform(self, url: str) -> str:
        """Convert IDC link to final Udemy link with coupon."""
        response = requests.get(url, allow_redirects=True, timeout=10)
        if 'udemy.com' not in response.url:
            udemy_url: str = self.scrape(url)
            return udemy_url
        self.logger.info('%s ==> %s', url, udemy_url)
        return response.url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from IDC."""
        self.logger.info('IDC bot starting...')
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                udemy_urls.add(udemy_url)
            except (RequestException, TimeoutException) as e:
                self.logger.exception('%s. Skipping...', e)
                continue
        return udemy_urls
