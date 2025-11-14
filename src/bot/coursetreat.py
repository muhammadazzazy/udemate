"""Encapsulate the Course Treat spider methods and attributes."""
import requests
import undetected_chromedriver as uc
from gotify import Gotify
from requests.exceptions import RequestException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider
from utils.config import BotConfig


class CourseTreat(Spider):
    """Course Treat spider to get Udemy links with coupons."""

    def __init__(self, urls: list[str], driver: uc.Chrome,
                 gotify: Gotify, config: BotConfig) -> None:
        self.driver = driver
        super().__init__(urls=urls, gotify=gotify,
                         retries=config.retries, timeout=config.timeout)

    def transform(self, url: str) -> str:
        """Return Udemy link from Course Treat link."""
        self.driver.get(url)
        enroll_url: str = self.driver.find_element(
            By.CLASS_NAME, 'btn-couponbtn',
        ).get_attribute('href')
        response: requests.Response = requests.get(
            enroll_url, timeout=self.timeout)
        count: int = 0
        while (count < self.retries) and ('coursetreat.com' in response.url):
            response = requests.get(enroll_url, timeout=self.timeout)
            count += 1
        udemy_url: str = self.clean(response.url)
        return udemy_url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from Course Treat."""
        self.logger.info('Processing %d intermediary links from Course Treat...',
                         len(self.urls))
        self.gotify.create_message(
            title='Course Treat spider started',
            message=f'Processing {len(self.urls)} intermediary links from Course Treat.'
        )
        udemy_urls: list[str] = []
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                udemy_urls.append(udemy_url)
            except WebDriverException as e:
                self.logger.error('Webdriver error for %s: %r', url, e)
                continue
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('Read timeout error for %s: %r', url, e)
                continue
            except RequestException as e:
                self.logger.error('Request exception for %s: %r', url, e)
                continue
        return udemy_urls
