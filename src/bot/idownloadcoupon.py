"""Fetch Udemy links with coupons from IDownloadCoupon."""
from urllib.parse import ParseResult, urlparse, parse_qs, unquote

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

from bot.spider import Spider
from config.bot import SpiderConfig


class IDownloadCoupon(Spider):
    """Get Udemy links with coupons from IDownloadCoupon."""

    def __init__(self, *, config: SpiderConfig, urls: list[str]) -> None:
        self.session = requests.Session()
        super().__init__(config=config, urls=urls)

    def transform(self, url: str) -> str | None:
        """Convert IDownloadCoupon link to final Udemy link with coupon."""
        for attempt in range(self.config.retries):
            try:
                response: requests.Response = self.session.get(
                    url, allow_redirects=True, timeout=self.config.timeout)
                soup: BeautifulSoup = BeautifulSoup(
                    response.text,
                    'html.parser'
                )
                not_found = soup.find(
                    'h3',
                    string=lambda text: text and text.strip() == '404 Page not found'
                )
                if not_found:
                    self.logger.warning('404 Page not found for %s', url)
                    return None

                clean_url: str = self.extract_udemy_link(
                    self.clean(response.url))

                if 'idownloadcoupon.com' in clean_url:
                    self.logger.warning('No Udemy redirect for %s', url)
                    continue
                self.logger.info('%s ==> %s', url, clean_url)
                return clean_url
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
