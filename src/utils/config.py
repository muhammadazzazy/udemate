"""Configure Udemate based on environment variables in .env file."""
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Final

from dotenv import load_dotenv

DEFAULT_USER_AGENT: Final[str] = 'Udemate:v1.0.0 (by u/kemitche)'

DEFAULT_LIMIT: Final[int] = 500
MAX_LIMIT: Final[int] = 1000

FORMATTED_DATE: Final[str] = datetime.today().strftime('%Y%m%d')
load_dotenv()


@dataclass
class Config:
    """Encapsulate and validate configuration attributes loaded from .env."""
    client_id: str
    client_secret: str
    user_agent: str
    limit: int
    password: str
    username: str

    def __init__(self) -> None:
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.user_agent = os.environ.get(
            'REDDIT_USER_AGENT', DEFAULT_USER_AGENT)
        self.limit = int(os.environ.get('LIMIT', DEFAULT_LIMIT))
        self.password = os.environ.get('REDDIT_PASSWORD')
        self.username = os.environ.get('REDDIT_USERNAME')
