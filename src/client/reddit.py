"""Configure Reddit PRAW for r/udemyfreebies, fetch posts on subreddit, and extract hostnames."""
from urllib.parse import urlparse

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
                client_id=self.config.reddit_client_id,
                client_secret=self.config.reddit_client_secret,
                user_agent=self.config.reddit_user_agent,
                refresh_token=refresh_token
            )
        else:
            self.reddit = praw.Reddit(
                client_id=self.config.reddit_client_id,
                client_secret=self.config.reddit_client_secret,
                password=self.config.reddit_password,
                user_agent=self.config.reddit_user_agent,
                username=self.config.reddit_username
            )
        self.submissions: list[Submission] = []
        self.logger = setup_logging()

    def populate_submissions(self, subreddit: str = 'udemyfreebies') -> None:
        """Fill the list of Reddit posts."""
        try:
            subreddit = self.reddit.subreddit(subreddit)
            for submission in subreddit.new(limit=self.config.reddit_limit):
                self.submissions.append(submission)
        except RequestException as e:
            self.logger.error('Failed to fetch Reddit posts: %r', e)

    def get_middlemen(self) -> list[str]:
        """Return list of detected middlemen hostnames."""
        middlemen: list[str] = []
        for submission in self.submissions:
            result = urlparse(submission.url)
            flag: bool = all(
                [result.scheme, result.netloc]
            )
            if not flag:
                continue
            standard_url: str = self.clean(submission.url)
            hostname: str = standard_url.split('/')[2]
            middleman: str = hostname.split('.')[0]
            if middleman not in middlemen:
                middlemen.append(middleman)

        return middlemen

    def get_middleman_urls(self, middlemen: list[str]) -> dict[str, list[str]]:
        """Return mapping between middlemen and submission links."""
        urls: dict[str, list[str]] = {}
        for middleman in middlemen:
            urls[middleman] = []
        for submission in self.submissions:
            for middleman in middlemen:
                if middleman in submission.url:
                    urls[middleman].append(self.clean(submission.url))
                    break
        for middleman in middlemen:
            urls[middleman] = sorted(set(urls[middleman]))
        return urls

    def clean(self, url: str) -> str:
        """Return cleaned middlemen link."""
        parts: list[str] = url.split('/')
        while '' in parts:
            parts.remove('')
        clean_url: str = parts[0] + '//' + '/'.join(parts[1:4])
        clean_url = clean_url.replace('www.', '')
        return clean_url
