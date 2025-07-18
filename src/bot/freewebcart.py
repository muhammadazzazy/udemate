"""Scrape Udemy links with coupons from Freewebcart."""
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import ProtocolError, ReadTimeoutError
from bot.spider import Spider


class Freewebcart(Spider):
    """Get Udemy links with coupons from Freewebcart."""

    def __init__(self, *, driver, urls: set[str]) -> None:
        super().__init__(urls)
        self.driver = driver

    def transform(self, url: str) -> str:
        """Return Udemy link from Freewebcart link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 30)
        link = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(text(), 'Get 100% OFF Coupon')]"))
        )
        udemy_url: str = link.get_attribute('href')
        return udemy_url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from Freewebcart."""
        self.logger.info('Freewebcart spider starting...')
        self.logger.info('Processing %d links from Freewebcart...',
                         len(self.urls))
        udemy_urls: set[str] = set()
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                udemy_urls.add(udemy_url)
            except TimeoutException as e:
                self.logger.error('Timeout while parsing %s: %r', url, e)
                continue
            except WebDriverException as e:
                self.logger.error('Webdriver error for %s: %r', url, e)
                continue
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('ReadTimeoutError error for %s: %r', url, e)
                continue
        self.logger.info('Freewebcart spider scraped %d Udemy links.',
                         len(udemy_urls))
        return udemy_urls
