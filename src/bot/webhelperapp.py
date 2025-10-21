"""Scrape Udemy links with coupons from WebHelperApp."""
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider


class WebHelperApp(Spider):
    """Get Udemy links with coupons from WebHelperApp."""

    def __init__(self, *, driver, urls: list[str]) -> None:
        super().__init__(urls)
        self.driver = driver

    def transform(self, url: str) -> str:
        """Return Udemy link from WebHelperApp link."""
        self.driver.get(url)
        link = self.driver.find_element(By.XPATH,
                                        "//a[contains(., 'GET COURSE')]")
        udemy_url: str = link.get_attribute('href')
        return udemy_url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from WebHelperApp."""
        self.logger.info('WebHelperApp spider starting...')
        self.logger.info('Processing %d links from WebHelperApp...',
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
        self.logger.info('WebHelperApp spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.driver.quit()
        return sorted(set(udemy_urls))
