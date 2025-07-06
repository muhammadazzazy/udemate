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
from utils.logger import setup_logging
from web.browser import Browser


class Udemate:
    """Control the flow of Udemate."""

    def __init__(self) -> None:
        self.config = Config()
        self.cache = Cache()
        self.browser = Browser()
        self.logger = setup_logging()
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
                             urls=self.cache.urls['udemy'])
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
        self.logger.info('Spiders scraped a total of %d Udemy links.',
                         len(udemy_urls))
        headless_driver.quit()
        return udemy_urls

    def run(self, args) -> None:
        """Coordinate program execution."""
        try:
            if args.mode in ('hybrid', 'gui'):
                self.cache.read_json('udemy.json')
                self.unlock()
            if args.mode == 'gui':
                return
            for middleman in self.middleman_classes:
                self.cache.read_json(f'{middleman}.json')
            if self.config.password:
                reddit_client: RedditClient = RedditClient()
            else:
                refresh_token: str = get_refresh_token(self.config)
                reddit_client: RedditClient = RedditClient(refresh_token)
            reddit_client.populate_submissions()
            hostnames: set[str] = set(self.middleman_classes.keys())
            middleman_urls: dict[str, set[str]
                                 ] = reddit_client.get_middleman_urls(hostnames)
            for middleman in self.middleman_classes:
                self.cache.write_json(
                    data=middleman_urls[middleman], filename=f'{middleman}.json')
            udemy_urls: set[str] = self.get_udemy_urls(middleman_urls)
            self.cache.write_json(data=udemy_urls, filename='udemy.json')
        except KeyboardInterrupt:
            sys.exit()
