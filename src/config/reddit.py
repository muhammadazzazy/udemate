"""Configuration model for Reddit client settings."""
from pydantic import BaseModel


class RedditConfig(BaseModel):
    """Encapsulate and validate Reddit client configuration attributes."""
    client_id: str | None
    client_secret: str | None
    user_agent: str | None
    username: str | None
    password: str | None


class SubredditConfig(BaseModel):
    """Encapsulate and validate subreddit configuration attributes."""
    name: str
    limit: int
