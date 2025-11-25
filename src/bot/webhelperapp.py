"""Scrape Udemy links with coupons from WebHelperApp."""
import undetected_chromedriver as uc
from gotify import Gotify
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider
from utils.config import BotConfig


class WebHelperApp(Spider):
    """Get Udemy links with coupons from WebHelperApp."""

    def __init__(self, *, driver: uc.Chrome, urls: list[str],
                 gotify: Gotify, config: BotConfig) -> None:
        self.driver = driver
        super().__init__(urls=urls, config=config, gotify=gotify)

    def transform(self, url: str) -> str:
        """Return Udemy link from WebHelperApp link."""
        self.driver.get(url)
        link: uc.WebElement = self.driver.find_element(By.XPATH,
                                                       "//a[contains(., 'GET COURSE')]")
        href: str = link.get_attribute('href')
        udemy_url: str = self.clean(href)
        return udemy_url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from WebHelperApp."""
        self.logger.info('Processing %d links from WebHelperApp...',
                         len(self.urls))
        self.gotify.create_message(
            title='WebHelperApp spider started',
            message=f'Processing {len(self.urls)} intermediary links from WebHelperApp.'
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
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error('Read timeout error for %s: %r', url, e)
                continue
        self.logger.info('WebHelperApp spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.gotify.create_message(
            title='WebHelperApp spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from WebHelperApp.'
        )
        self.driver.quit()
        return sorted(set(udemy_urls))
