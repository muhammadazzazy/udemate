"""Configure Udemate based on environment variables in .env file."""
from typing import Final
from datetime import datetime

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_USER_AGENT: Final[str] = 'Udemate:v1.0.0 (by u/kemitche)'
DEFAULT_LIMIT: Final[int] = 500
MIN_LIMIT: Final[int] = 1
MAX_LIMIT: Final[int] = 1000

FORMATTED_DATE: Final[str] = datetime.today().strftime('%Y%m%d')


class Config(BaseSettings):
    """Encapsulate and validate configuration attributes loaded from .env."""
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      case_sensitive=True)
    REDDIT_CLIENT_ID: str = Field(description='Reddit script client ID')
    REDDIT_CLIENT_SECRET: str = Field(
        description='Reddit script client secret')
    REDDIT_USER_AGENT: str = Field(
        default=DEFAULT_USER_AGENT, description='Reddit script user agent')
    REDDIT_LIMIT: int = Field(DEFAULT_LIMIT,
                              le=MAX_LIMIT,
                              ge=MIN_LIMIT,
                              description='Maximum number of posts parsed by Reddit script')
    REDDIT_PASSWORD: str = Field(
        description='Password of Reddit account')
    REDDIT_USERNAME: str = Field(
        description='Username of Reddit account')
    BROWSER_USER_DATA_DIR: str = Field(
        description='Path to Brave Browser user data directory'
    )
    BROWSER_MAJOR_VERSION: int = Field(
        description='Major version of the Chromium browser installed on the system'
    )
