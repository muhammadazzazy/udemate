"""Configure Udemate based on environment variables in .env file."""
import os
from dataclasses import asdict, dataclass

from typing import Final

from dotenv import load_dotenv

DEFAULT_USER_AGENT: Final[str] = 'Udemate:v1.0.0 (by u/kemitche)'

DEFAULT_LIMIT: Final[int] = 500
MAX_LIMIT: Final[int] = 1000

load_dotenv()


@dataclass
class Config:
    """Encapsulate and validate configuration attributes loaded from .env."""
    client_id: str
    client_secret: str
    user_agent: str
    limit: int

    def __init__(self) -> None:
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.user_agent = os.environ.get(
            'REDDIT_USER_AGENT', DEFAULT_USER_AGENT)
        self.limit = int(os.environ.get('LIMIT', DEFAULT_LIMIT))

    def __post_init__(self) -> None:
        missing: list[str] = []
        if not all(asdict(self).values()):
            raise ValueError(
                f'Missing environment variable(s): {', '.join(missing)}')
        if asdict(self)['limit'] > MAX_LIMIT:
            print(f"Max value for 'LIMIT' is {MAX_LIMIT}...")
            self.limit = MAX_LIMIT
