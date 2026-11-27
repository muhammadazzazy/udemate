"""
Configure Reddit PRAW for r/udemyfreebies, r/udemyfreeebies, and r/udemyfreecourses subreddits,
fetch posts on subreddit, and extract hostnames.
"""
import re
from logging import Logger
from urllib.parse import urlparse

import praw
from prawcore.exceptions import RequestException
from praw.models.reddit.submission import Submission
from praw.models.reddit.subreddit import Subreddit

from config.reddit import RedditConfig, SubredditConfig


class RedditClient:
    """
    Configure Reddit client for various subreddits, get subreddit posts,
    and map hostnames to submission links.
    """

    def __init__(self, *, config: RedditConfig, subreddit_configs: list[SubredditConfig],
                 refresh_token: str | None = None, logger: Logger) -> None:
        self.config = config
        self.subreddit_configs = subreddit_configs
        self.logger = logger
        if refresh_token:
            self.refresh_token = refresh_token
            self.reddit = praw.Reddit(
                client_id=config.client_id,
                client_secret=config.client_secret,
                user_agent=config.user_agent,
                refresh_token=refresh_token
            )
        else:
            self.reddit = praw.Reddit(
                client_id=config.client_id,
                client_secret=config.client_secret,
                password=config.password,
                user_agent=config.user_agent,
                username=config.username
            )
        self.submissions: list[Submission] = []

    def populate_submissions(self) -> None:
        """Fill the list of Reddit posts."""
        try:
            subreddits: list[Subreddit] = [
                self.reddit.subreddit(config.name) for config in self.subreddit_configs
            ]
            for i, subreddit in enumerate(subreddits):
                for submission in subreddit.new(limit=self.subreddit_configs[i].limit):
                    self.submissions.append(submission)
        except RequestException as e:
            self.logger.error('Failed to fetch Reddit posts: %r', e)

    def get_intermediaries(self) -> list[str]:
        """Return list of detected intermediaries hostnames."""
        intermediaries: list[str] = []
        for submission in self.submissions:
            result = urlparse(submission.url)
            flag: bool = all(
                [result.scheme, result.netloc]
            )
            if not flag:
                continue
            standard_url: str = self.clean(submission.url)
            hostname: str = standard_url.split('/')[2]
            intermediary: str = hostname.split('.')[0]
            if intermediary not in intermediaries:
                intermediaries.append(intermediary)

        return intermediaries

    def parse_markdown(self, markdown: str) -> list[str]:
        """Return list of intermediary URLs from Reddit post selftext."""
        pattern: str = r'\*\s+(.*?)\s+\[REDEEM OFFER\]\((https?://[^)]+)\)'
        matches: list[tuple[str, str]] = re.findall(pattern, markdown)
        intermediary_urls: list[str] = []
        for _title, url in matches:
            intermediary_urls.append(self.clean(url))
        return sorted(set(intermediary_urls))

    def clean(self, url: str) -> str:
        """Return clean intermediaries link."""
        parts: list[str] = url.split('/')
        while '' in parts:
            parts.remove('')
        clean_url: str = parts[0] + '//' + '/'.join(parts[1:4])
        clean_url = clean_url.replace('www.', '')
        return clean_url

    def collect_intermediary_urls(self, intermediaries: list[str]) -> dict[str, list[str]]:
        """Return mapping between intermediaries and submission links."""
        urls: dict[str, list[str]] = {}
        for intermediary in intermediaries:
            urls[intermediary] = []
        udemy_urls: list[str] = []
        for submission in self.submissions:
            if submission.selftext:
                udemy_urls.extend(self.parse_markdown(
                    submission.selftext))
            if submission.url:
                udemy_urls.append(self.clean(submission.url))
        for intermediary in intermediaries:
            for url in udemy_urls:
                hostname: str = url.split('/')[2]
                intermediary_hostname: str = hostname.split('.')[0]
                if intermediary == intermediary_hostname:
                    urls[intermediary].append(url)
        for intermediary in intermediaries:
            urls[intermediary] = sorted(set(urls[intermediary]))
        return urls
