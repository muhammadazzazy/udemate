"""Configure Reddit PRAW for r/udemyfreebies, fetch posts on subreddit, and extract hostnames."""
from typing import Final
from urllib.parse import urlparse

import praw
from praw.models.reddit.submission import Submission

from utils.config import Config


SUBREDDIT_NAME: Final[str] = 'udemyfreebies'


class RedditClient:
    """Configure Reddit client for r/udemyfreebies subreddit,
    get subreddit posts, and extract hostnames."""

    def __init__(self, refresh_token: str) -> None:
        self.config = Config()
        self.refresh_token = refresh_token
        self.reddit = praw.Reddit(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            user_agent=self.config.user_agent,
            refresh_token=refresh_token
        )
        self.submissions: list[Submission] = []

    def populate_submissions(self) -> None:
        """Return list of Reddit submissions."""
        subreddit = self.reddit.subreddit(SUBREDDIT_NAME)
        for submission in subreddit.new(limit=self.config.limit):
            self.submissions.append(submission)

    def get_hostnames(self, submissions: list[Submission]) -> set[str]:
        """Return set of hostnames."""
        hostnames: set[str] = set()
        for submission in submissions:
            domain: str = urlparse(submission.url).netloc
            parts: list[str] = domain.split('.')
            if 'reddit' not in domain and domain:
                if domain.startswith('www.'):
                    hostname: str = parts[1]
                else:
                    hostname: str = parts[0]
                hostnames.add(hostname)
        return hostnames

    def get_middleman_urls(self, hostnames) -> dict[str, set[str]]:
        """Return mapping between hostnames and submission links."""
        urls: dict[str, set[str]] = {
            hostname: set() for hostname in hostnames
        }
        for submission in self.submissions:
            for hostname in hostnames:
                if hostname in submission.url:
                    urls[hostname].add(submission.url)
        return urls
