"""Scrape Udemy links with coupons from EasyLearning."""
import requests
from requests.exceptions import RequestException

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from bot.spider import Spider


class EasyLearning(Spider):
    """Get Udemy links with coupons from EasyLearning."""

    def scrape(self, url: str) -> str:
        """Return Udemy link from EasyLearning link."""
        self.driver.get(url)
        enroll_url: str = self.driver.find_element(
            By.CSS_SELECTOR, "a.purple-button").get_attribute('href')
        response = requests.get(enroll_url, timeout=20)
        udemy_url: str = response.url
        return udemy_url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from Easylearning."""
        self.logger.info('Easy Learning bot starting...')
        self.logger.info('Processing %d intermediary links from Easy Learning...',
                         len(self.urls))
        udemy_urls: set[str] = set()
        max_len: int = len(max(self.urls, key=len))
        for url in self.urls:
            try:
                udemy_url: str = self.scrape(url)
                self.logger.info('%-*s ==> %s', max_len, url, udemy_url)
                udemy_urls.add(udemy_url)
            except (RequestException, WebDriverException):
                self.logger.warning('Something went wrong. Skipping...')
                continue
        self.logger.info('Easy Learning bot scraped %d Udemy links.',
                         len(udemy_urls))
        return udemy_urls
