"""
Parse Udemy links with coupons from cache, automate course enrollment,
scrape middleman links, get new Udemy links with coupons, and write them back to cache.
"""
from selenium.webdriver.chrome.webdriver import WebDriver

from bot.spider_meta import SPIDERS
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

    def setup_reddit_client(self) -> RedditClient:
        """Return Reddit client for r/udemyfreebies."""
        if self.config.REDDIT_PASSWORD:
            reddit_client: RedditClient = RedditClient()
        else:
            refresh_token: str = get_refresh_token(self.config)
            reddit_client: RedditClient = RedditClient(refresh_token)
        return reddit_client

    def collect_middleman_links(self) -> dict[str, set[str]]:
        """Collect middleman links from Reddit."""
        reddit_client: RedditClient = self.setup_reddit_client()
        reddit_client.populate_submissions()
        hostnames: set[str] = set(SPIDERS.keys())
        middleman_urls: dict[str, list[str]
                             ] = reddit_client.get_middleman_urls(hostnames)
        for sld in SPIDERS:
            self.cache.write_json(data=middleman_urls[sld],
                                  filename=f'{sld}.json')
        return middleman_urls

    def scrape(self) -> None:
        """Fetch collection of Udemy links with coupons using middleman bots."""
        middleman_urls: dict[str, set[str]] = self.collect_middleman_links()
        udemy_urls: list[str] = []
        headless_driver: WebDriver = self.browser.setup(headless=True)
        for key, cls in SPIDERS.items():
            if key == 'idownloadcoupon':
                spider = cls.spider_cls(middleman_urls[key])
            else:
                spider = cls.spider_cls(driver=headless_driver,
                                        urls=middleman_urls[key])
            if key in middleman_urls:
                udemy_urls.extend(spider.run())
        udemy_urls.sort()
        self.logger.info('Spiders scraped a total of %d Udemy links.',
                         len(udemy_urls))
        headless_driver.quit()
        self.cache.write_json(data=udemy_urls, filename='udemy.json')

    def autoenroll(self) -> None:
        """
        Read unprocessed Udemy links from cache, automate enrollment into free Udemy courses, 
        and clear cache.
        """
        filename: str = 'udemy.json'
        exists: bool = self.cache.read_json(filename)
        if not exists:
            self.logger.info('Exiting...')
            return
        processed_urls: list[str] = self.cache.read_jsonl('udemy.jsonl')
        self.logger.debug('Processed URLs: %s', processed_urls)
        self.cache.urls['udemy'] = sorted(set(
            self.cache.urls['udemy']) - set(processed_urls))
        gui_driver: WebDriver = self.browser.setup(headless=False)
        udemy: Udemy = Udemy(
            driver=gui_driver,
            cache=self.cache
        )
        udemy.run()
        gui_driver.quit()
        self.logger.info('Clearing Udemy cache...')
        self.cache.delete_json(filename)
