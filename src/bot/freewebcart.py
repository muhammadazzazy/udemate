"""Scrape Udemy links with coupons from Freewebcart."""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import setup_logging


class Freewebcart:
    """Get Udemy links with coupons from Freewebcart."""

    def __init__(self, driver: WebDriver, urls: set[str]) -> None:
        self.driver = driver
        self.urls = urls
        self.logger = setup_logging()

    def scrape(self, url) -> str:
        """Return Udemy link from Freewebcart link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 20)
        link = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(), "🎁 Get 100% OFF Coupon")]'))
        )
        return link.get_attribute("href")

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from Freewebcart."""
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                udemy_url: str = self.scrape(url)
                udemy_urls.add(udemy_url)
            except TimeoutException as e:
                self.logger.exception('%s. Skipping...', e)
                continue
        return udemy_urls
