"""
Parse Udemy links with coupons from cache, automate course enrollment,
scrape middleman links, get new Udemy links with coupons, and write them back to cache.
"""
import json
from pathlib import Path
from typing import Any
from selenium.webdriver.chrome.webdriver import WebDriver

from bot.easy_learning import EasyLearning
from bot.freewebcart import Freewebcart
from bot.idownloadcoupon import IDownloadCoupon
from bot.invent_high import InventHigh
from bot.line51 import Line51
from bot.webhelperapp import WebHelperApp
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

    def get_middlemen(self) -> list[str]:
        """Return list of middlemen from 'middlemen.json' configuration file."""
        middlemen_path: Path = Path(
            __file__).parent.parent.parent / 'config' / 'middlemen.json'
        if not middlemen_path.exists():
            self.logger.error('Middlemen configuration file not found.')
            raise FileNotFoundError('middlemen.json not found.')
        middlemen: list[str] = []
        with middlemen_path.open('r', encoding='utf-8') as f:
            middlemen = json.load(f)
        return middlemen

    def setup_reddit_client(self) -> RedditClient:
        """Return Reddit client for r/udemyfreebies."""
        if self.config.REDDIT_PASSWORD:
            reddit_client: RedditClient = RedditClient()
        else:
            refresh_token: str = get_refresh_token(self.config)
            reddit_client: RedditClient = RedditClient(refresh_token)
        return reddit_client

    def collect_middleman_links(self, middlemen: list[str]) -> dict[str, set[str]]:
        """Collect middleman links from Reddit."""
        reddit_client: RedditClient = self.setup_reddit_client()
        reddit_client.populate_submissions()
        middleman_urls: dict[str,
                             list[str]] = reddit_client.get_middleman_urls(middlemen)
        for middleman in middlemen:
            self.cache.write_json(
                data=middleman_urls[middleman],
                filename=f'{middleman}.json'
            )
        return middleman_urls

    def initialize_spiders(self, middleman_urls: dict[str, set[str]]) -> dict[str, Any]:
        """Initialize spiders for each middleman."""
        headless_driver: WebDriver = self.browser.setup(headless=True)
        spiders: dict[str, Any] = {
            'easylearn': EasyLearning(
                driver=headless_driver,
                urls=middleman_urls['easylearn'],
            ),
            'idownloadcoupon': IDownloadCoupon(
                urls=middleman_urls['idownloadcoupon'],
            ),
            'freewebcart': Freewebcart(
                driver=headless_driver,
                urls=middleman_urls['freewebcart']
            ),
            'inventhigh': InventHigh(
                driver=headless_driver,
                urls=middleman_urls['inventhigh']
            ),
            'line51': Line51(
                driver=headless_driver,
                urls=middleman_urls['line51']
            ),
            'webhelperapp': WebHelperApp(
                driver=headless_driver,
                urls=middleman_urls['webhelperapp']
            )
        }
        headless_driver.quit()
        return spiders

    def scrape(self, middlemen: list[str]) -> None:
        """Fetch collection of Udemy links with coupons using middleman spiders."""
        middleman_urls: dict[str, set[str]
                             ] = self.collect_middleman_links(middlemen)
        udemy_urls: list[str] = []

        spiders: dict[str, Any] = self.initialize_spiders(middleman_urls)
        for middleman, spider in spiders.items():
            if middleman in middlemen:
                udemy_urls.extend(spider.run())

        udemy_urls.sort()
        self.logger.info('Spiders scraped a total of %d Udemy links.',
                         len(udemy_urls))
        self.cache.write_json(data=udemy_urls, filename='udemy.json')

    def autoenroll(self) -> None:
        """
        Read unprocessed Udemy links from cache, automate enrollment into free Udemy courses, 
        and clear cache.
        """
        if not self.cache.read_json('udemy.json'):
            self.logger.info('Exiting...')
            return
        processed_urls: list[str] = self.cache.read_jsonl('udemy.jsonl')
        self.cache.urls['udemy'] = sorted(set(
            self.cache.urls['udemy']) - set(processed_urls))
        gui_driver: WebDriver = self.browser.setup(headless=False)
        udemy: Udemy = Udemy(
            driver=gui_driver,
            cache=self.cache
        )
        udemy.run()
        gui_driver.quit()
