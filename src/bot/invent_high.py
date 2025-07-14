"""Scrape Udemy links with coupons from Invent High."""
import requests

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import ReadTimeoutError

from bot.spider import Spider


class InventHigh(Spider):
    """Get Udemy links with coupons from Invent High."""

    def scrape(self, url: str) -> str:
        """Return Udemy link from Invent High link."""
        self.driver.get(url)
        link = self.driver.find_element(By.ID, 'couponval')
        url: str = link.get_attribute('href')
        response = requests.get(url, timeout=20)
        udemy_url: str = response.url
        return udemy_url

    def run(self) -> None:
        """Return set of Udemy links extracted from Line51."""
        self.logger.info('Line51 spider starting...')
        self.logger.info('Processing %d links from Line51...',
                         len(self.urls))
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                udemy_url: str = self.scrape(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                udemy_urls.add(udemy_url)
            except TimeoutException as e:
                self.logger.error('Timeout while parsing %s: %s', url, e)
                continue
            except WebDriverException as e:
                self.logger.error('WebDriver error for %s: %s', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('ReadTimeoutError error for %s: %s', url, e)
                continue
        self.logger.info('Line51 spider scraped %d Udemy links.',
                         len(udemy_urls))
        return udemy_urls
