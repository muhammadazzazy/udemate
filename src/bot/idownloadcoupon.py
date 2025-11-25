"""Fetch Udemy links with coupons from iDC."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import ParseResult, urlparse, parse_qs, unquote

import requests
from gotify import Gotify

from bot.spider import Spider
from utils.config import BotConfig


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from iDC."""

    def __init__(self, *, urls: list[str],
                 gotify: Gotify, config: BotConfig) -> None:
        self.session = requests.Session()
        super().__init__(urls=urls, config=config, gotify=gotify)

    def transform(self, url: str) -> str | None:
        """Convert iDC link to final Udemy link with coupon."""
        response: requests.Response = self.session.get(
            url, allow_redirects=True, timeout=self.timeout)
        count: int = 0
        while (count < self.retries) and ('idownloadcoupon.com' in url):
            response = self.session.get(
                url, allow_redirects=True, timeout=self.timeout)
            count += 1
        if 'idownloadcoupon.com' in response.url:
            return None
        udemy_url: str = self.extract_udemy_link(self.clean(response.url))
        self.logger.info('%s ==> %s', url, udemy_url)
        return udemy_url

    def extract_udemy_link(self, url: str) -> str:
        """Return Udemy link from LinkSynergy affiliate link."""
        parsed_url: ParseResult = urlparse(url)
        query_params: dict = parse_qs(parsed_url.query)
        murl: str | None = query_params.get('murl', [None])[0]
        if murl:
            return unquote(murl)
        return url

    def run(self) -> list[str]:
        """Return list of Udemy links extracted from IDownloadCoupon."""
        self.logger.info('Processing %d links from IDownloadCoupon...',
                         len(self.urls))
        self.gotify.create_message(
            title='iDC spider started',
            message=f'Processing {len(self.urls)} intermediary links from iDC.'
        )
        udemy_urls: list[str] = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(
                self.transform, url): url for url in self.urls}
            for future in as_completed(futures):
                result: str | None = future.result()
                if result:
                    udemy_urls.append(result)
        self.logger.info('iDC spider scraped %d Udemy links.', len(udemy_urls))
        self.gotify.create_message(
            title='iDC spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from iDC.'
        )
        return sorted(set(udemy_urls))
