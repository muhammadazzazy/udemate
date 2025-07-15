"""Scrape Udemy links with coupons from EasyLearning."""
import requests
from requests.exceptions import RequestException

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import ReadTimeoutError

from bot.spider import Spider


class EasyLearning(Spider):
    """Get Udemy links with coupons from EasyLearning."""

    def scrape(self, url: str) -> str:
        """Return Udemy link from EasyLearning link."""
        self.driver.get(url)
        enroll_url: str = self.driver.find_element(
            By.CSS_SELECTOR, "a.purple-button").get_attribute('href')
        response = requests.get(enroll_url, timeout=30)
        udemy_url: str = response.url
        return udemy_url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from Easylearning."""
        self.logger.info('Easy Learning spider starting...')
        self.logger.info('Processing %d intermediary links from Easy Learning...',
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
            except RequestException as e:
                self.logger.error('HTTP request failed for %s: %s', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('ReadTimeoutError error for %s: %s', url, e)
                continue
        self.logger.info('Easy Learning spider scraped %d Udemy links.',
                         len(udemy_urls))
        return udemy_urls
