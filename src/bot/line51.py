"""Scrape Udemy links with coupons from Line51."""
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider


class Line51(Spider):
    """Get Udemy links with coupons from Line51."""

    def __init__(self, *, driver, urls: list[str]) -> None:
        super().__init__(urls)
        self.driver = driver

    def transform(self, url: str) -> str:
        """Return Udemy link from Line51 link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 30)
        link = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(), "Get Discount Now")]'))
        )
        udemy_url: str = self.clean(link.get_attribute('href'))
        return udemy_url

    def run(self) -> None:
        """Return set of Udemy links extracted from Line51."""
        self.logger.info('Line51 spider starting...')
        self.logger.info('Processing %d links from Line51...',
                         len(self.urls))
        udemy_urls: list[str] = []
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                udemy_urls.append(udemy_url)
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
                self.logger.error('Read timeout error for %s: %r', url, e)
                continue
        self.logger.info('Line51 spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.driver.quit()
        return sorted(set(udemy_urls))
