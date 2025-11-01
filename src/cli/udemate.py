"""
Parse Udemy links with coupons from cache, automate course enrollment,
scrape middleman links, get new Udemy links with coupons, and write them back to cache.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from logging import Logger
from typing import Any

import undetected_chromedriver as uc

from bot.coursecouponz import CourseCouponz
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
from web.brave import Brave
from web.google_chrome import GoogleChrome


class Udemate:
    """Control the flow of Udemate."""

    def __init__(self, *, config: Config, logger: Logger) -> None:
        if 'brave' in config.user_data_dir.lower():
            self.browser = Brave(
                major_version=141,
                user_data_dir=config.user_data_dir,
                logger=logger)
        elif 'chrome' in config.user_data_dir.lower():
            self.browser = GoogleChrome(
                major_version=141,
                user_data_dir=config.user_data_dir,
                logger=logger)
        self.cache = Cache()
        self.config = config
        self.logger = logger

    def setup_reddit_client(self) -> RedditClient:
        """Return Reddit client for r/udemyfreebies."""
        if self.config.reddit_password:
            reddit_client: RedditClient = RedditClient()
        else:
            refresh_token: str = get_refresh_token(self.config)
            reddit_client: RedditClient = RedditClient(refresh_token)
        return reddit_client

    def collect_middleman_links(self) -> dict[str, set[str]]:
        """Collect middleman links from Reddit."""
        reddit_client: RedditClient = self.setup_reddit_client()
        reddit_client.populate_submissions()
        middlemen: list[str] = reddit_client.get_middlemen()
        middleman_urls: dict[
            str,
            list[str]
        ] = reddit_client.get_middleman_urls(middlemen)
        for middleman in middlemen:
            self.cache.write_json(
                data=middleman_urls[middleman],
                filename=f'{middleman}.json'
            )
        return middleman_urls

    def initialize_spiders(self, middleman_urls: dict[str, set[str]]) -> dict[str, Any]:
        """Initialize spiders for each middleman."""
        spiders: dict[str, Any] = {}
        for middleman, urls in middleman_urls.items():
            match middleman:
                case 'coursecouponz':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = CourseCouponz(
                        driver=headless_driver,
                        urls=urls,
                        retries=self.config.coursecouponz_retries,
                        timeout=self.config.coursecouponz_timeout
                    )
                case 'easylearn':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = EasyLearning(
                        driver=headless_driver,
                        urls=urls,
                        retries=self.config.easylearn_retries,
                        timeout=self.config.easylearn_timeout
                    )
                case 'freewebcart':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = Freewebcart(
                        driver=headless_driver,
                        urls=urls,
                        retries=self.config.freewebcart_retries,
                        timeout=self.config.freewebcart_timeout
                    )
                case 'idownloadcoupon':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = IDownloadCoupon(
                        urls=urls,
                        retries=self.config.idc_retries,
                        timeout=self.config.idc_timeout
                    )
                case 'inventhigh':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = InventHigh(
                        driver=headless_driver,
                        urls=urls,
                        retries=self.config.inventhigh_retries,
                        timeout=self.config.inventhigh_timeout
                    )
                case 'line51':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = Line51(
                        driver=headless_driver,
                        urls=urls,
                        retries=self.config.line51_retries,
                        timeout=self.config.line51_timeout
                    )
                case 'webhelperapp':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = WebHelperApp(
                        driver=headless_driver,
                        urls=urls,
                        retries=self.config.webhelperapp_retries,
                        timeout=self.config.webhelperapp_timeout
                    )
        return spiders

    def scrape(self) -> list[str]:
        """Fetch collection of Udemy links with coupons using middleman spiders."""
        middleman_urls: dict[str, set[str]] = self.collect_middleman_links()
        udemy_urls: list[str] = []
        spiders: dict[str, Any] = self.initialize_spiders(middleman_urls)
        with ThreadPoolExecutor(max_workers=min(8, len(spiders))) as executor:
            futures = {executor.submit(
                spider.run): middleman for middleman, spider in spiders.items()}
            for future in as_completed(futures):
                __name: str = futures[future]
                result: list[str] = future.result()
                udemy_urls.extend(result)
        udemy_urls = sorted(set(udemy_urls))
        self.logger.info('Spiders scraped a total of %d Udemy links.',
                         len(udemy_urls))
        self.cache.write_json(data=udemy_urls, filename='udemy.json')
        return udemy_urls

    def autoenroll(self, udemy_urls: list[str]) -> None:
        """Autoenroll into free Udemy courses using GUI browser."""
        udemy_urls: list[str] = self.cache.filter_urls('udemy')
        gui_driver: uc.Chrome = self.browser.setup(headless=False)
        udemy: Udemy = Udemy(
            driver=gui_driver,
            retries=self.config.udemy_retries,
            timeout=self.config.udemy_timeout,
            urls=udemy_urls,
        )
        udemy.run()
        gui_driver.quit()

    def run(self, mode: str) -> None:
        """Run Udemate based on command-line arguments passed."""
        self.logger.info('Starting Udemate in %s mode...', mode)
        udemy_urls: list[str] = []
        if mode in ('headless', 'hybrid'):
            udemy_urls: list[str] = self.scrape()
        if mode in ('hybrid', 'gui'):
            self.autoenroll(udemy_urls)
