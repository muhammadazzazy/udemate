"""Fetch Udemy links with coupons from iDC."""
from urllib.parse import ParseResult, urlparse, parse_qs, unquote

import requests
from gotify import Gotify
from requests.exceptions import RequestException
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from bot.spider import Spider
from utils.config import BotConfig


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from iDC."""

    def __init__(self, *, urls: list[str],
                 gotify: Gotify, config: BotConfig) -> None:
        self.session = requests.Session()
        super().__init__(urls=urls, gotify=gotify,
                         retries=config.retries, timeout=config.timeout)

    def transform(self, url: str) -> str | None:
        """Convert iDC link to final Udemy link with coupon."""
        response: requests.Response = self.session.get(
            url, allow_redirects=True, timeout=self.timeout)
        count: int = 0
        while (count < self.retries) and ('idownloadcoupon.com' in url):
            response = self.session.get(
                url, allow_redirects=True, timeout=self.timeout)
            count += 1
        if 'idownloadcoupon.com' in url:
            return None
        udemy_url: str = self.extract_udemy_link(self.clean(response.url))
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
        for url in self.urls:
            try:
                udemy_url: str = self.transform(url)
                self.logger.info('%s ==> %s', url, udemy_url)
                if udemy_url:
                    udemy_urls.append(udemy_url)
            except RequestException as e:
                self.logger.error(
                    'HTTP request failed for %s: %r', url, e)
                continue
            except ProtocolError as e:
                self.logger.error('Protocol error for %s: %r', url, e)
                continue
            except ReadTimeoutError as e:
                self.logger.error(
                    'Read timeout error for %s: %r', url, e)
                continue
        self.logger.info('iDC spider scraped %d Udemy links.', len(udemy_urls))
        self.gotify.create_message(
            title='iDC spider finished',
            message=f'Scraped {len(udemy_urls)} Udemy links from iDC.'
        )
        return sorted(set(udemy_urls))
