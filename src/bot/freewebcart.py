"""Scrape Udemy links with coupons from Freewebcart."""
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bot.base import Bot


class Freewebcart(Bot):
    """Get Udemy links with coupons from Freewebcart."""

    def scrape(self, url: str) -> str:
        """Return Udemy link from Freewebcart link."""
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 30)
        link = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//a[contains(text(), "🎁 Get 100% OFF Coupon")]'))
        )
        udemy_url: str = link.get_attribute("href")
        return udemy_url

    def run(self) -> set[str]:
        """Return set of Udemy links extracted from Freewebcart."""
        self.logger.info('Freewebcart bot starting...')
        udemy_urls: set[str] = set()
        self.logger.info('Processing %d links from Freewebcart...',
                         len(udemy_urls))
        max_len: int = max(self.urls, key=len)
        for url in self.urls:
            try:
                udemy_url: str = self.scrape(url)
                self.logger.info('%-*s ==> %s', max_len, url, udemy_url)
                udemy_urls.add(udemy_url)
            except WebDriverException as e:
                self.logger.exception('%s. Skipping...', e)
                continue
        self.logger.info('Freewebcart bot collected %d links.',
                         len(udemy_urls))
        return udemy_urls
