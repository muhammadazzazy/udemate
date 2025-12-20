"""Implements RealDiscount spider for converting middleman links to Udemy links."""
import requests
import undetected_chromedriver as uc
from gotify import Gotify
from requests.exceptions import RequestException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from bot.spider import Spider
from config.bot import SpiderConfig


class RealDiscount(Spider):
    """Encapsulates methods to scrape Udemy links from RealDiscount."""

    def __init__(self, config: SpiderConfig, driver: uc.Chrome,
                 gotify: Gotify, urls: list[str]) -> None:
        self.session = requests.Session()
        self.driver = driver
        super().__init__(config=config, gotify=gotify, urls=urls)

    def transform(self, url: str) -> str | None:
        """Return Udemy link from WebHelperApp link."""
        for attempt in range(self.config.retries):
            try:
                self.driver.get(url)
                wait: WebDriverWait = WebDriverWait(
                    self.driver, self.config.timeout
                )
                link: uc.WebElement = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//a[contains(text(), 'Get Course')]"))
                )
                href: str = link.get_attribute('href')
                udemy_url: str | None = self.clean(href)
                self.logger.info('%s ==> %s', url, udemy_url)
                return udemy_url
            except RequestException as e:
                self.logger.error(
                    'Attempt %d: Error fetching %s: %s', attempt+1, url, str(e)
                )
                continue
        return None
