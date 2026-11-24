"""Convert Deelcart (formely Freewebcart) links to Udemy links."""
from logging import Logger

import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider
from config.bot import SpiderConfig


class Deelcart(Spider):
    """Get Udemy links with coupons from Deelcart."""

    def __init__(self, *, driver: uc.Chrome, urls: list[str],
                 config: SpiderConfig, logger: Logger) -> None:
        self.driver = driver
        super().__init__(urls=urls, config=config, logger=logger)

    def transform(self, url: str) -> str:
        """Return Udemy link from Deelcart link."""
        self.driver.get(url)
        wait: WebDriverWait = WebDriverWait(self.driver, self.config.timeout)
        redirect_link: uc.WebElement = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href^='/redirect/']")
            )
        )
        redirect_href: str = redirect_link.get_attribute('href')
        redirect_url: str = urljoin('https://deelcart.com', redirect_href)

        self.driver.get(redirect_url)
        udemy_link: uc.WebElement = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href*='udemy.com/course/']")
            )
        )
        href: str = udemy_link.get_attribute('href')
        udemy_url: str = self.clean(href)
        return udemy_url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from Deelcart."""
        self.logger.info('Processing %d links from Deelcart...',
                         len(self.urls))
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
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('Read timeout error for %s: %r', url, e)
                continue
        self.logger.info('Deelcart spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.driver.quit()
        return sorted(set(udemy_urls))
