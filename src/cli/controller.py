"""
Parse Udemy links with coupons from cache, automate course enrollment,
scrape middleman links, get new Udemy links with coupons, and write them back to cache.
"""
from bot.freewebcart import Freewebcart
from bot.idownloadcoupon import IDownloadCoupon
from bot.udemy import Udemy
from client.get_refresh_token import get_refresh_token
from client.reddit import RedditClient
from utils.cache import Cache
from utils.config import Config
from web.setup_browser import setup_brave


class Controller:
    """Control the flow of Udemate."""

    def __init__(self) -> None:
        self.config = Config()
        self.cache = Cache()
        self.middleman_classes = {
            'freewebcart': Freewebcart,
            'idownloadcoupon': IDownloadCoupon
        }

    def unlock(self) -> None:
        """Unlock Udemy courses found in cache."""
        udemy_driver = setup_brave(headless=False)
        udemy: Udemy = Udemy(driver=udemy_driver,
                             urls=self.cache.udemy_urls)
        udemy.run()
        udemy_driver.quit()

    def get_udemy_urls(self, middleman_urls: dict[str, set[str]]) -> set[str]:
        """Fetch collection of Udemy links with coupons using middleman bots."""
        udemy_urls: set[str] = set()
        headless_driver = setup_brave(headless=True)
        for key, cls in self.middleman_classes.items():
            if key in middleman_urls:
                bot: Freewebcart | IDownloadCoupon = cls(
                    driver=headless_driver, urls=middleman_urls[key])
                udemy_urls.update(bot.run())
        headless_driver.quit()
        return udemy_urls

    def run(self) -> None:
        """Coordinate program execution."""
        self.cache.read()
        if self.cache.udemy_urls:
            self.unlock()
        refresh_token: str = get_refresh_token(self.config)
        reddit_client: RedditClient = RedditClient(refresh_token)
        reddit_client.populate_submissions()
        hostnames: set[str] = reddit_client.get_hostnames(
            reddit_client.submissions)
        middleman_urls: dict[str, set[str]
                             ] = reddit_client.get_middleman_urls(hostnames)
        udemy_urls: set[str] = self.get_udemy_urls(middleman_urls)
        print(udemy_urls)
        self.cache.write(data=udemy_urls)
