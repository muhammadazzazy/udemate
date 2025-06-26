"""Scrape Udemy links with coupons from EasyLearning."""
import requests

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from bot.base import Bot


class EasyLearning(Bot):
    """Get Udemy links with coupons from EasyLearning."""

    def scrape(self, url: str) -> str:
        """Return Udemy link from EasyLearning link."""
        self.driver.get(url)
        enroll_url: str = self.driver.find_element(
            By.CSS_SELECTOR, "a.purple-button").get_attribute('href')
        response = requests.get(enroll_url, timeout=10)
        udemy_url: str = response.url
        self.logger.info('%s ==> %s', url, udemy_url)
        return udemy_url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from Easylearning."""
        self.logger.info('Easy Learning bot starting...')
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                udemy_url: str = self.scrape(url)
                udemy_urls.add(udemy_url)
            except WebDriverException as e:
                self.logger.exception('%s. Skipping...', e)
                continue
        self.logger.info('Easy Learning bot collected %d links.',
                         len(udemy_urls))
        return udemy_urls
