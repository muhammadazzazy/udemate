"""Scrape Udemy links with coupons from Invent High."""
import requests
from requests import RequestException

import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider


class InventHigh(Spider):
    """Get Udemy links with coupons from Invent High."""

    def __init__(self, *, driver: uc.Chrome, urls: list[str], retries: int, timeout: int) -> None:
        self.driver = driver
        super().__init__(urls=urls, retries=retries, timeout=timeout)

    def transform(self, url: str) -> str:
        """Return Udemy link from Invent High link."""
        self.driver.get(url)
        wait: WebDriverWait = WebDriverWait(self.driver, self.timeout)
        link: uc.WebElement = wait.until(
            EC.visibility_of_element_located(
                (By.ID, 'couponval'))
        )
        url: str = link.get_attribute('href')
        response: requests.Response = requests.get(url, timeout=30)
        udemy_url: str = self.clean(response.url)
        return udemy_url

    def is_coupon_expired(self, url: str) -> bool:
        """Check if Invent High coupon has expired."""
        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, self.timeout)
            _text: str = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[text()='---------Expired---------']")
                )
            )
            self.logger.info('Coupon expired for %s', url)
            return True
        except TimeoutException:
            return False

    def run(self) -> None:
        """Return list of Udemy links extracted from Invent High."""
        self.logger.info('Invent High spider starting...')
        self.logger.info('Processing %d links from Invent High...',
                         len(self.urls))
        udemy_urls: list[str] = []
        for url in self.urls:
            try:
                if self.is_coupon_expired(url):
                    continue
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                udemy_urls.append(udemy_url)
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
        self.logger.info('Invent High spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.driver.quit()
        return sorted(set(udemy_urls))
