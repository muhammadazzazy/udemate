"""Configure Udemate based on environment variables in .env file."""
from typing import Final, Optional
from datetime import datetime

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_USER_AGENT: Final[str] = 'Udemate:v1.0.0 (by u/kemitche)'
DEFAULT_SUBREDDIT_LIMIT: Final[int] = 500
MIN_SUBREDDIT_LIMIT: Final[int] = 0
MAX_SUBREDDIT_LIMIT: Final[int] = 1000

DEFAULT_BROWSER_MAJOR_VERSION: Final[int] = 142

BOT_DEFAULTS: Final[dict[str, dict[str, int]]] = {
    'coursecouponz': {'retries': 3, 'threads': 2, 'timeout': 30},
    'coursetreat': {'retries': 3, 'threads': 2, 'timeout': 30},
    'easylearn': {'retries': 3, 'threads': 10, 'timeout': 30},
    'freewebcart': {'retries': 3, 'threads': 2, 'timeout': 30},
    'idownloadcoupon': {'retries': 3, 'threads': 25, 'timeout': 30},
    'inventhigh': {'retries': 3, 'threads': 2, 'timeout': 30},
    'line51': {'retries': 3, 'threads': 2, 'timeout': 30},
    'webhelperapp': {'retries': 3, 'threads': 2, 'timeout': 30},
    'udemy': {'retries': 3, 'timeout': 10}
}

FORMATTED_DATE: Final[str] = datetime.today().strftime('%Y%m%d')


class Settings(BaseSettings):
    """Encapsulate and validate configuration attributes loaded from .env."""
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

    browser_major_version: int = Field(
        description='Major version of the browser to be automated',
        default=DEFAULT_BROWSER_MAJOR_VERSION
    )
    user_data_dir: str = Field(
        description='Path to Brave Browser user data directory'
    )

    coursecouponz_retries: int = Field(
        description='Maximum number of retries for Course Couponz requests',
        default=BOT_DEFAULTS['coursecouponz']['retries']
    )
    coursecouponz_threads: int = Field(
        description='Number of threads for Course Couponz requests',
        default=BOT_DEFAULTS['coursecouponz']['threads']
    )
    coursecouponz_timeout: int = Field(
        description='Timeout (in seconds) for Course Couponz requests',
        default=BOT_DEFAULTS['coursecouponz']['timeout']
    )

    coursetreat_retries: int = Field(
        description='Maximum number of retries for Course Treat requests',
        default=BOT_DEFAULTS['coursetreat']['retries']
    )
    coursetreat_threads: int = Field(
        description='Number of threads for Course Treat requests',
        default=BOT_DEFAULTS['coursetreat']['threads']
    )
    coursetreat_timeout: int = Field(
        description='Timeout (in seconds) for Course Treat requests',
        default=BOT_DEFAULTS['coursetreat']['timeout']
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

    freewebcart_retries: int = Field(
        description='Maximum number of retries for Freewebcart requests and actions',
        default=BOT_DEFAULTS['freewebcart']['retries']
    )
    freewebcart_threads: int = Field(
        description='Number of threads for Freewebcart requests and actions',
        default=BOT_DEFAULTS['freewebcart']['threads']
    )
    freewebcart_timeout: int = Field(
        description='Timeout (in seconds) for Freewebcart web requests and actions',
        default=BOT_DEFAULTS['freewebcart']['timeout']
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

    line51_retries: int = Field(
        description='Maximum number of retries for Line51 requests and actions',
        default=BOT_DEFAULTS['line51']['retries']
    )
    line51_threads: int = Field(
        description='Number of threads for Line51 requests and actions',
        default=2
    )
    line51_timeout: int = Field(
        description='Timeout (in seconds) for Line51 requests and actions',
        default=BOT_DEFAULTS['line51']['timeout']
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

    udemy_email: str = Field(
        description='Email address for Udemy account',
    )
    udemy_retries: int = Field(
        description='Maximum number of retries for web actions such as enrollments',
        default=BOT_DEFAULTS['udemy']['retries']
    )
    udemy_timeout: int = Field(
        description='Timeout (in seconds) for web actions such as enrollments',
        default=BOT_DEFAULTS['udemy']['timeout']
    )

    gotify_base_url: str = Field(
        description='Base URL of Gotify server'
    )
    gotify_app_token: str = Field(
        description='Application token for Gotify notifications'
    )
