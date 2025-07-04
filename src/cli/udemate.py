"""
Parse Udemy links with coupons from cache, automate course enrollment,
scrape middleman links, get new Udemy links with coupons, and write them back to cache.
"""
import sys

from selenium.webdriver.chrome.webdriver import WebDriver

from bot.easylearning import EasyLearning
from bot.freewebcart import Freewebcart
from bot.idownloadcoupon import IDownloadCoupon
from bot.line51 import Line51
from bot.udemy import Udemy
from client.get_refresh_token import get_refresh_token
from client.reddit import RedditClient
from utils.cache import Cache
from utils.config import Config
from web.browser import Browser


class Udemate:
    """Control the flow of Udemate."""

    def __init__(self) -> None:
        self.config = Config()
        self.cache = Cache()
        self.browser = Browser()
        self.middleman_classes = {
            'easylearn.ing': EasyLearning,
            'idownloadcoupon': IDownloadCoupon,
            'line51': Line51,
            'freewebcart': Freewebcart,
        }

    def unlock(self) -> None:
        """Unlock Udemy courses found in cache."""
        udemy_driver: WebDriver = self.browser.setup(headless=False)
        udemy: Udemy = Udemy(driver=udemy_driver,
                             urls=self.cache.udemy_urls)
        udemy.run()
        udemy_driver.quit()

    def get_udemy_urls(self, middleman_urls: dict[str, set[str]]) -> set[str]:
        """Fetch collection of Udemy links with coupons using middleman bots."""
        udemy_urls: set[str] = set()
        headless_driver: WebDriver = self.browser.setup(headless=True)
        for key, cls in self.middleman_classes.items():
            if key in middleman_urls:
                bot = cls(driver=headless_driver, urls=middleman_urls[key])
                udemy_urls.update(bot.run())
        headless_driver.quit()
        return udemy_urls

    def run(self) -> None:
        """Coordinate program execution."""
        try:
            self.cache.read_json()
            if self.cache.udemy_urls:
                self.unlock()
            if self.config.password:
                reddit_client: RedditClient = RedditClient()
            else:
                refresh_token: str = get_refresh_token(self.config)
                reddit_client: RedditClient = RedditClient(refresh_token)
            reddit_client.populate_submissions()
            hostnames: set[str] = set(self.middleman_classes.keys())
            middleman_urls: dict[str, set[str]
                                 ] = reddit_client.get_middleman_urls(hostnames)
            udemy_urls: set[str] = self.get_udemy_urls(middleman_urls)
            self.cache.write_json(data=udemy_urls)
        except KeyboardInterrupt:
            sys.exit()
