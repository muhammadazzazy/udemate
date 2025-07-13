"""Configure Reddit PRAW for r/udemyfreebies, fetch posts on subreddit, and extract hostnames."""
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
                self.submissions.append(submission)
        except RequestException as e:
            self.logger.error('RequestException: %s', e)

    def get_middleman_urls(self, hostnames: set[str]) -> dict[str, set[str]]:
        """Return mapping between hostnames and submission links."""
        urls: dict[str, set[str]] = {
            hostname: set() for hostname in hostnames
        }
        for submission in self.submissions:
            for hostname in hostnames:
                if hostname in submission.url:
                    urls[hostname].add(submission.url)
        return urls
