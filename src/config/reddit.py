"""Configuration model for Reddit client settings."""
from pydantic import BaseModel


class RedditConfig(BaseModel):
    """Encapsulate and validate Reddit client configuration attributes."""
    client_id: str
    client_secret: str
    user_agent: str
    username: str
    password: str


class SubredditConfig(BaseModel):
    """Encapsulate and validate subreddit configuration attributes."""
    name: str
    limit: int
