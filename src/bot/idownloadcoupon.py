"""Fetch Udemy links with coupons from iDC."""
from urllib.parse import ParseResult, urlparse, parse_qs, unquote

import requests
from gotify import Gotify
from requests.exceptions import RequestException

from bot.spider import Spider
from utils.config import SpiderConfig


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from iDC."""

    def __init__(self, *, config: SpiderConfig, urls: list[str],
                 gotify: Gotify) -> None:
        self.session = requests.Session()
        super().__init__(config=config, gotify=gotify, urls=urls)

    def transform(self, url: str) -> str | None:
        """Convert iDC link to final Udemy link with coupon."""
        for attempt in range(self.config.retries):
            try:
                response: requests.Response = self.session.get(
                    url, allow_redirects=True, timeout=self.config.timeout)
                udemy_url: str = self.extract_udemy_link(
                    self.clean(response.url))
                self.logger.info('%s ==> %s', url, udemy_url)
                if 'idownloadcoupon' in udemy_url:
                    continue
                return udemy_url
            except RequestException as e:
                self.logger.error(
                    'Attempt %d: Error fetching %s: %s', attempt+1, url, str(e)
                )
                continue
        return None

    def extract_udemy_link(self, url: str) -> str:
        """Return Udemy link from LinkSynergy affiliate link."""
        parsed_url: ParseResult = urlparse(url)
        query_params: dict = parse_qs(parsed_url.query)
        murl: str | None = query_params.get('murl', [None])[0]
        if murl:
            return unquote(murl)
        return url
