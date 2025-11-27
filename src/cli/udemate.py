"""
Parse Udemy links with coupons from cache, automate course enrollment,
scrape middleman links, get new Udemy links with coupons, and write them back to cache.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from logging import Logger
from typing import Any

import undetected_chromedriver as uc

from bot.coursecouponz import CourseCouponz
from bot.coursetreat import CourseTreat
from bot.easy_learning import EasyLearning
from bot.freewebcart import Freewebcart
from bot.idownloadcoupon import IDownloadCoupon
from bot.invent_high import InventHigh
from bot.line51 import Line51
from bot.webhelperapp import WebHelperApp
from bot.udemy import Udemy
from client.get_refresh_token import get_refresh_token
from client.gotify import GotifyClient
from client.reddit import RedditClient
from utils.cache import Cache
from utils.config import BotConfig, Config, SpiderConfig
from web.brave import Brave
from web.google_chrome import GoogleChrome


class Udemate:
    """Control the flow of Udemate."""

    def __init__(self, *, config: Config, gotify: GotifyClient, logger: Logger) -> None:
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
        self.gotify = gotify
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
                    spiders[middleman] = CourseCouponz(
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.coursecouponz_retries,
                            threads=self.config.coursecouponz_threads,
                            timeout=self.config.coursecouponz_timeout
                        )
                    )
                case 'coursetreat':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = CourseTreat(
                        driver=headless_driver,
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.coursetreat_retries,
                            threads=self.config.coursetreat_threads,
                            timeout=self.config.coursetreat_timeout
                        )
                    )
                case 'easylearn':
                    spiders[middleman] = EasyLearning(
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.easylearn_retries,
                            threads=self.config.easylearn_threads,
                            timeout=self.config.easylearn_timeout
                        )
                    )
                case 'freewebcart':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = Freewebcart(
                        driver=headless_driver,
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.freewebcart_retries,
                            threads=self.config.freewebcart_threads,
                            timeout=self.config.freewebcart_timeout
                        )
                    )
                case 'idownloadcoupon':
                    spiders[middleman] = IDownloadCoupon(
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.idc_retries,
                            threads=self.config.idc_threads,
                            timeout=self.config.idc_timeout
                        )
                    )
                case 'inventhigh':
                    spiders[middleman] = InventHigh(
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.inventhigh_retries,
                            threads=self.config.inventhigh_threads,
                            timeout=self.config.inventhigh_timeout
                        )
                    )
                case 'line51':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = Line51(
                        driver=headless_driver,
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.line51_retries,
                            threads=self.config.line51_threads,
                            timeout=self.config.line51_timeout
                        )
                    )
                case 'webhelperapp':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = WebHelperApp(
                        driver=headless_driver,
                        urls=urls,
                        gotify=self.gotify,
                        config=SpiderConfig(
                            retries=self.config.webhelperapp_retries,
                            threads=self.config.webhelperapp_threads,
                            timeout=self.config.webhelperapp_timeout
                        )
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
        self.gotify.create_message(
            title='Scraping completed',
            message=f'Spiders scraped a total of {len(udemy_urls)} Udemy links.'
        )
        self.logger.info('Spiders scraped a total of %d Udemy links.',
                         len(udemy_urls))
        self.cache.write_json(data=udemy_urls, filename='udemy.json')
        return udemy_urls

    def autoenroll(self, udemy_urls: list[str]) -> None:
        """Autoenroll into free Udemy courses using GUI browser."""
        udemy_urls: list[str] = self.cache.filter_urls('udemy')
        if not udemy_urls:
            self.logger.info('No new Udemy links to process. Exiting...')
            return
        gui_driver: uc.Chrome = self.browser.setup(headless=False)
        udemy: Udemy = Udemy(
            driver=gui_driver,
            config=BotConfig(
                retries=self.config.udemy_retries,
                timeout=self.config.udemy_timeout
            ),
            urls=udemy_urls,
            gotify=self.gotify
        )
        udemy.run(email=self.config.udemy_email)
        gui_driver.quit()

    def run(self, mode: str) -> None:
        """Run Udemate based on command-line arguments passed."""
        self.gotify.create_message(
            title='Udemate started',
            message=f'Udemate is starting in {mode} mode.'
        )
        self.logger.info('Starting Udemate in %s mode...', mode)
        udemy_urls: list[str] = []
        if mode in ('headless', 'hybrid'):
            udemy_urls: list[str] = self.scrape()
        if mode in ('hybrid', 'gui'):
            self.autoenroll(udemy_urls)
