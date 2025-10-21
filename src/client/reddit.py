"""Configure Reddit PRAW for r/udemyfreebies, fetch posts on subreddit, and extract hostnames."""
from sys import exit

import praw
from prawcore.exceptions import RequestException
from praw.models.reddit.submission import Submission

from utils.config import Config
from utils.logger import setup_logging


class RedditClient:
    """Configure Reddit client for r/udemyfreebies subreddit,
    get subreddit posts, and map hostnames to submission links."""

    def __init__(self, refresh_token: str | None = None) -> None:
        self.config = Config()
        if refresh_token:
            self.refresh_token = refresh_token
            self.reddit = praw.Reddit(
                client_id=self.config.REDDIT_CLIENT_ID,
                client_secret=self.config.REDDIT_CLIENT_SECRET,
                user_agent=self.config.REDDIT_USER_AGENT,
                refresh_token=refresh_token
            )
        else:
            self.reddit = praw.Reddit(
                client_id=self.config.REDDIT_CLIENT_ID,
                client_secret=self.config.REDDIT_CLIENT_SECRET,
                password=self.config.REDDIT_PASSWORD,
                user_agent=self.config.REDDIT_USER_AGENT,
                username=self.config.REDDIT_USERNAME
            )
        self.submissions: list[Submission] = []
        self.logger = setup_logging()

    def populate_submissions(self, subreddit: str = 'udemyfreebies') -> None:
        """Fill the list of Reddit posts."""
        try:
            subreddit = self.reddit.subreddit(subreddit)
            for submission in subreddit.new(limit=self.config.REDDIT_LIMIT):
                self.logger.info('Adding Reddit post with URL: %s',
                                 submission.url)
                self.submissions.append(submission)
        except RequestException as e:
            self.logger.error('RequestException: %s', e)
            exit()

    def get_middleman_urls(self, hostnames: list[str]) -> dict[str, list[str]]:
        """Return mapping between hostnames and submission links."""
        urls: dict[str, list[str]] = {
            hostname: [] for hostname in hostnames
        }
        for submission in self.submissions:
            for hostname in hostnames:
                if hostname in submission.url:
                    urls[hostname].append(self.clean(submission.url))
        for hostname in hostnames:
            urls[hostname] = sorted(set(urls[hostname]))
        return urls

    def clean(self, url: str) -> str:
        """Return cleaned middlemen link."""
        parts: list[str] = url.split('/')
        while '' in parts:
            parts.remove('')
        clean_url: str = parts[0] + '//' + '/'.join(parts[1:4])
        return clean_url
