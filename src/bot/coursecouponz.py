"""Scrape Udemy links with coupons from CourseCouponz."""
import undetected_chromedriver as uc
from gotify import Gotify
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

from bot.spider import Spider
from utils.config import BotConfig


class CourseCouponz(Spider):
    """Get Udemy links with coupons from CourseCouponz."""

    def __init__(self, *, driver: uc.Chrome, urls: list[str],
                 gotify: Gotify, config: BotConfig) -> None:
        self.driver = driver
        super().__init__(urls=urls, gotify=gotify,
                         retries=config.retries, timeout=config.timeout)

    def transform(self, url: str) -> str:
        """Return Udemy link from CourseCouponz link."""
        self.driver.get(url)
        link: uc.WebElement = self.driver.find_element(
            By.XPATH,
            "//a[contains(., 'GET COURSE')]"
        )
        count: int = 0
        while (count < self.retries) and ('coursecouponz.com' in link.get_attribute('href')):
            link = self.driver.find_element(
                By.XPATH,
                "//a[contains(., 'GET COURSE')]"
            )
            count += 1
        udemy_url: str = self.clean(link.get_attribute('href'))
        return udemy_url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from CourseCouponz."""
        self.logger.info('Processing %d intermediary links from CourseCouponz...',
                         len(self.urls))
        self.gotify.create_message(
            title='CourseCouponz spider started',
            message=f'Processing {len(self.urls)} intermediary links from CourseCouponz.'
        )
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
        self.logger.info('CourseCouponz spider scraped %d Udemy links.',
                         len(udemy_urls))
        self.gotify.create_message(
            title='CourseCouponz spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from CourseCouponz.'
        )
        self.driver.quit()
        return sorted(set(udemy_urls))
