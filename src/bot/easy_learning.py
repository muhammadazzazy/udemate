"""Scrape Udemy links with coupons from Easy Learning."""
import requests
from requests.exceptions import RequestException

import undetected_chromedriver as uc
from gotify import Gotify
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider
from utils.config import BotConfig


class EasyLearning(Spider):
    """Get Udemy links with coupons from Easy Learning."""

    def __init__(self, *, driver: uc.Chrome, urls: list[str],
                 gotify: Gotify, config: BotConfig) -> None:
        self.driver = driver
        super().__init__(urls=urls, config=config, gotify=gotify)

    def transform(self, url: str) -> str | None:
        """Return Udemy link from Easy Learning link."""
        self.driver.get(url)
        enroll_url: str = self.driver.find_element(
            By.CSS_SELECTOR, 'a.purple-button').get_attribute('href')
        response: requests.Response = requests.get(
            enroll_url, timeout=self.timeout)
        count: int = 0
        while (count < self.retries) and ('easylearn.ing' in response.url):
            response = requests.get(enroll_url, timeout=self.timeout)
            count += 1
        if 'easylearn.ing' in response.url:
            return None
        udemy_url: str = self.clean(response.url)
        return udemy_url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from Easy Learning."""
        self.logger.info('Processing %d intermediary links from Easy Learning...',
                         len(self.urls))
        self.gotify.create_message(
            title='Easy Learning spider started',
            message=f'Processing {len(self.urls)} intermediary links from Easy Learning.'
        )
        udemy_urls: list[str] = []
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                if udemy_url:
                    self.logger.info('%s ==> %s', url, udemy_url)
                    udemy_urls.append(udemy_url)
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

        self.logger.info('Easy Learning spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.gotify.create_message(
            title='Easy Learning spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from Easy Learning.'
        )
        self.driver.quit()
        return sorted(set(udemy_urls))
