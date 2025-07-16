"""Scrape Udemy links with coupons from Line51."""
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider


class Line51(Spider):
    """Get Udemy links with coupons from Line51."""

    def scrape(self, url: str) -> str:
        """Return Udemy link from Line51 link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 30)
        link = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(), "Get Discount Now")]'))
        )
        udemy_url: str = link.get_attribute('href')
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
                self.logger.error('WebDriver for %s: %s', url, e)
                continue
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %s', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('Read timeout error for %s: %s', url, e)
                continue
        self.logger.info('Line51 spider scraped %d Udemy links.',
                         len(udemy_urls))
        return udemy_urls
