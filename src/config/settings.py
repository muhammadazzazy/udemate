"""Configure Udemate based on environment variables in .env file."""
from datetime import datetime
from pathlib import Path
from typing import Final, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Final[str] = Path(__file__).resolve().parent.parent.parent
DEFAULT_USER_AGENT: Final[str] = 'Udemate:v1.0.0 (by u/kemitche)'
DEFAULT_SUBREDDIT_LIMIT: Final[int] = 500
MIN_SUBREDDIT_LIMIT: Final[int] = 0
MAX_SUBREDDIT_LIMIT: Final[int] = 1000

BOT_DEFAULTS: Final[dict[str, dict[str, int]]] = {
    'easylearn': {'retries': 3, 'threads': 10, 'timeout': 30},
    'deelcart': {'retries': 3, 'threads': 2, 'timeout': 30},
    'idownloadcoupon': {'retries': 3, 'threads': 25, 'timeout': 30},
    'inventhigh': {'retries': 3, 'threads': 2, 'timeout': 30},
    'realdiscount': {'retries': 3, 'threads': 2, 'timeout': 30},
    'webhelperapp': {'retries': 3, 'threads': 2, 'timeout': 30},
    'udemy': {'retries': 3, 'timeout': 10}
}

FORMATTED_DATE: Final[str] = datetime.today().strftime('%Y%m%d')


class HeadlessSettings(BaseSettings):
    """Encapsulate and validate headless configuration attributes loaded from .env file."""
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      case_sensitive=False)
    reddit_client_id: str = Field(description='Reddit script client ID')
    reddit_client_secret: str = Field(
        description='Reddit script client secret')
    reddit_user_agent: str = Field(
        default=DEFAULT_USER_AGENT, description='Reddit script user agent')
    reddit_password: str = Field(
        description='Password of Reddit account')
    reddit_username: str = Field(
        description='Username of Reddit account')

    udemy_freebies_limit: int = Field(
        default=DEFAULT_SUBREDDIT_LIMIT,
        le=MAX_SUBREDDIT_LIMIT,
        ge=MIN_SUBREDDIT_LIMIT,
        description='Maximum number of posts parsed from r/udemyfreebies subreddit'
    )

    udemy_freeebies_limit: int = Field(
        default=DEFAULT_SUBREDDIT_LIMIT,
        le=MAX_SUBREDDIT_LIMIT,
        ge=MIN_SUBREDDIT_LIMIT,
        description='Maximum number of posts parsed from r/udemyfreeebies subreddit'
    )

    udemy_free_courses_limit: int = Field(
        default=DEFAULT_SUBREDDIT_LIMIT,
        le=MAX_SUBREDDIT_LIMIT,
        ge=MIN_SUBREDDIT_LIMIT,
        description='Maximum number of posts parsed from r/udemyfreecourses subreddit'
    )

    user_data_dir: str = Field(
        description='Path to Chrome browser user data directory'
    )

    easylearn_retries: int = Field(
        description='Maximum number of retries for Easy Learning requests',
        default=BOT_DEFAULTS['easylearn']['retries']
    )
    easylearn_threads: int = Field(
        description='Number of threads for Easy Learning requests',
        default=BOT_DEFAULTS['easylearn']['threads']
    )
    easylearn_timeout: int = Field(
        description='Timeout (in seconds) for Easy Learning requests and actions',
        default=BOT_DEFAULTS['easylearn']['timeout']
    )

    deelcart_retries: int = Field(
        description='Maximum number of retries for Deelcart requests and actions',
        default=BOT_DEFAULTS['deelcart']['retries']
    )
    deelcart_threads: int = Field(
        description='Number of threads for Deelcart requests and actions',
        default=BOT_DEFAULTS['deelcart']['threads']
    )
    deelcart_timeout: int = Field(
        description='Timeout (in seconds) for Deelcart web requests and actions',
        default=BOT_DEFAULTS['deelcart']['timeout']
    )

    idownloadcoupon_retries: int = Field(
        description='Maximum number of retries for IDownloadCoupon requests',
        default=BOT_DEFAULTS['idownloadcoupon']['retries']
    )
    idownloadcoupon_threads: int = Field(
        description='Number of threads for IDownloadCoupon requests',
        default=BOT_DEFAULTS['idownloadcoupon']['threads']
    )
    idownloadcoupon_timeout: int = Field(
        description='Timeout (in seconds) for IDownloadCoupon requests',
        default=BOT_DEFAULTS['idownloadcoupon']['timeout']
    )

    inventhigh_retries: int = Field(
        description='Maximum number of retries for InventHigh requests and actions',
        default=BOT_DEFAULTS['inventhigh']['retries']
    )
    inventhigh_threads: int = Field(
        description='Number of threads for InventHigh requests and actions',
        default=BOT_DEFAULTS['inventhigh']['threads']
    )
    inventhigh_timeout: int = Field(
        description='Timeout (in seconds) for InventHigh requests and actions',
        default=BOT_DEFAULTS['inventhigh']['timeout']
    )

    real_discount_retries: int = Field(
        description='Maximum number of retries for RealDiscount requests and actions',
        default=BOT_DEFAULTS['realdiscount']['retries']
    )
    real_discount_threads: int = Field(
        description='Number of threads for RealDiscount requests and actions',
        default=BOT_DEFAULTS['realdiscount']['threads']
    )
    real_discount_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for RealDiscount requests and actions',
        default=BOT_DEFAULTS['realdiscount']['timeout']
    )

    webhelperapp_retries: int = Field(
        description='Maximum number of retries for WebHelperApp requests and actions',
        default=BOT_DEFAULTS['webhelperapp']['retries']
    )
    webhelperapp_threads: int = Field(
        description='Number of threads for WebHelperApp requests and actions',
        default=BOT_DEFAULTS['webhelperapp']['threads']
    )
    webhelperapp_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for WebHelperApp requests and actions',
        default=BOT_DEFAULTS['webhelperapp']['timeout']
    )

    data_dir: Path = Field(
        description='Directory for cached data'
    )
    logs_dir: Path = Field(
        description='Directory for application logs'
    )

    telegram_session_name: str = Field(
        description='Session name for Telegram client',
        default='udemate'
    )
    telegram_api_id: int | None = Field(
        description='Telegram API ID for Telegram client',
    )
    telegram_api_hash: str | None = Field(
        description='Telegram API hash for Telegram client',
    )


class Settings(HeadlessSettings):
    """Encapsulate headless and GUI configuration attributes loaded from .env file."""
    udemy_email: str = Field(
        description='Email address for Udemy account',
    )

    gmail_client_secret: str = Field(
        description='Path to Gmail API credentials file',
        default=BASE_DIR / 'sso' / 'client_secret.json'
    )

    udemy_retries: int = Field(
        description='Maximum number of retries for web actions such as enrollments',
        default=BOT_DEFAULTS['udemy']['retries']
    )
    udemy_timeout: int = Field(
        description='Timeout (in seconds) for web actions such as enrollments',
        default=BOT_DEFAULTS['udemy']['timeout']
    )
