"""
Parse Udemy links with coupons from cache, automate course enrollment,
scrape middleman links, get new Udemy links with coupons, and write them back to cache.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from logging import Logger
from typing import Any

import undetected_chromedriver as uc

from bot.easy_learning import EasyLearning
from bot.deelcart import Deelcart
from bot.idownloadcoupon import IDownloadCoupon
from bot.invent_high import InventHigh
from bot.real_discount import RealDiscount
from bot.webhelperapp import WebHelperApp
from bot.udemy import Udemy
from client.get_refresh_token import get_refresh_token
from client.reddit import RedditClient
from client.telegram import TelegramBot
from utils.cache import Cache
from config.bot import BotConfig, SpiderConfig
from config.reddit import RedditConfig, SubredditConfig
from config.settings import Settings
from web.brave import Brave
from web.google_chrome import GoogleChrome


class Udemate:
    """Control the flow of Udemate."""

    def __init__(self, *, settings: Settings, logger: Logger) -> None:
        if 'brave' in settings.user_data_dir.lower():
            self.browser = Brave(
                user_data_dir=settings.user_data_dir,
                logger=logger)
        elif 'chrome' in settings.user_data_dir.lower():
            self.browser = GoogleChrome(
                user_data_dir=settings.user_data_dir,
                logger=logger)
        self.cache = Cache(data_dir=settings.data_dir, logger=logger)
        self.config = settings
        self.logger = logger

    def setup_reddit_client(self) -> RedditClient | None:
        """Return Reddit client associated with various subreddits."""
        if not self.config.reddit_client_id or not self.config.reddit_client_secret:
            self.logger.warning(
                'Reddit client ID and secret are required to collect middleman links.'
            )
            return None
        reddit_config = RedditConfig(
            client_id=self.config.reddit_client_id,
            client_secret=self.config.reddit_client_secret,
            password=self.config.reddit_password,
            user_agent=self.config.reddit_user_agent,
            username=self.config.reddit_username
        )
        subreddit_configs: list[SubredditConfig] = [
            SubredditConfig(
                name='udemyfreebies',
                limit=self.config.udemy_freebies_limit),
            SubredditConfig(
                name='udemyfreeebies',
                limit=self.config.udemy_freeebies_limit),
            SubredditConfig(
                name='udemyfreecourses',
                limit=self.config.udemy_free_courses_limit)
        ]
        if self.config.reddit_password:
            reddit_client: RedditClient = RedditClient(
                config=reddit_config,
                subreddit_configs=subreddit_configs,
                logger=self.logger
            )
        else:
            refresh_token: str = get_refresh_token(reddit_config)
            reddit_client: RedditClient = RedditClient(
                config=reddit_config, subreddit_configs=subreddit_configs,
                refresh_token=refresh_token, logger=self.logger
            )
        return reddit_client

    def collect_reddit_links(self) -> dict[str, list[str]]:
        """Collect middleman links from Reddit."""
        reddit_client: RedditClient | None = self.setup_reddit_client()
        if not reddit_client:
            return {}
        reddit_client.populate_submissions()
        reddit_middlemen: list[str] = reddit_client.get_middlemen()
        reddit_links: dict[
            str,
            list[str]
        ] = reddit_client.get_middleman_urls(reddit_middlemen)
        return reddit_links

    def collect_telegram_links(self) -> dict[str, list[str]]:
        """Collect middleman links from Telegram."""
        if not self.config.telegram_api_id or not self.config.telegram_api_hash:
            self.logger.warning(
                'Telegram API ID and hash are required. Skipping Deelcart and InventHigh links.'
            )
            return {}
        telegram_bot: TelegramBot = TelegramBot(
            name=self.config.telegram_session_name,
            api_id=self.config.telegram_api_id,
            api_hash=self.config.telegram_api_hash,
            logger=self.logger
        )
        telegram_links: dict[str, list[str]] = telegram_bot.run()
        return telegram_links

    def initialize_spiders(self, middleman_urls: dict[str, set[str]]) -> dict[str, Any]:
        """Initialize spiders for each middleman."""
        spiders: dict[str, Any] = {}
        for middleman, urls in middleman_urls.items():
            match middleman:
                case 'deelcart':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = Deelcart(
                        driver=headless_driver,
                        urls=urls,
                        config=SpiderConfig(
                            retries=self.config.deelcart_retries,
                            threads=self.config.deelcart_threads,
                            timeout=self.config.deelcart_timeout
                        ), logger=self.logger
                    )
                case 'easylearn':
                    spiders[middleman] = EasyLearning(
                        urls=urls,
                        config=SpiderConfig(
                            retries=self.config.easylearn_retries,
                            threads=self.config.easylearn_threads,
                            timeout=self.config.easylearn_timeout
                        ), logger=self.logger
                    )
                case 'idownloadcoupon':
                    spiders[middleman] = IDownloadCoupon(
                        urls=urls,
                        config=SpiderConfig(
                            retries=self.config.idownloadcoupon_retries,
                            threads=self.config.idownloadcoupon_threads,
                            timeout=self.config.idownloadcoupon_timeout
                        ), logger=self.logger
                    )
                case 'inventhigh':
                    spiders[middleman] = InventHigh(
                        urls=urls,
                        config=SpiderConfig(
                            retries=self.config.inventhigh_retries,
                            threads=self.config.inventhigh_threads,
                            timeout=self.config.inventhigh_timeout
                        ), logger=self.logger
                    )
                case 'real':
                    headless_driver: uc.Chrome = self.browser.setup(
                        headless=True)
                    spiders[middleman] = RealDiscount(
                        driver=headless_driver,
                        urls=urls,
                        config=SpiderConfig(
                            retries=self.config.real_discount_retries,
                            threads=self.config.real_discount_threads,
                            timeout=self.config.real_discount_timeout
                        ), logger=self.logger
                    )
                case 'webhelperapp':
                    spiders[middleman] = WebHelperApp(
                        urls=urls,
                        config=SpiderConfig(
                            retries=self.config.webhelperapp_retries,
                            threads=self.config.webhelperapp_threads,
                            timeout=self.config.webhelperapp_timeout
                        ), logger=self.logger
                    )
        return spiders

    def scrape(self) -> list[str]:
        """Fetch collection of Udemy links with coupons using middleman spiders."""
        reddit_urls: dict[str, list[str]] = self.collect_reddit_links()
        telegram_urls: dict[str, list[str]] = self.collect_telegram_links()
        middleman_urls: dict[str, list[str]] = {**reddit_urls, **telegram_urls}
        udemy_urls: list[str] = []
        spiders: dict[str, Any] = self.initialize_spiders(middleman_urls)
        if len(spiders) == 0:
            self.logger.warning(
                'No middleman links to scrape. Exiting...'
            )
            return []
        with ThreadPoolExecutor(max_workers=min(8, len(spiders))) as executor:
            futures = {executor.submit(
                spider.run): middleman for middleman, spider in spiders.items()}
            for future in as_completed(futures):
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
        if not udemy_urls:
            self.logger.info('No new Udemy links to process. Exiting...')
            return
        gui_driver: uc.Chrome = self.browser.setup(headless=False)
        udemy: Udemy = Udemy(
            driver=gui_driver,
            cache=self.cache,
            config=BotConfig(
                retries=self.config.udemy_retries,
                timeout=self.config.udemy_timeout,
                gmail_client_secret=self.config.gmail_client_secret
            ),
            logger=self.logger,
            urls=udemy_urls
        )
        udemy.run(email=self.config.udemy_email)
        gui_driver.quit()

    def run(self, mode: str) -> None:
        """Run Udemate based on command-line arguments passed."""
        self.logger.info('Starting Udemate in %s mode...', mode)
        udemy_urls: list[str] = []
        if mode in ('headless', 'hybrid'):
            udemy_urls: list[str] = self.scrape()
        if mode in ('hybrid', 'gui'):
            self.autoenroll(udemy_urls)
