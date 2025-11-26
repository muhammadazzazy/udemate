"""Configure Udemate based on environment variables in .env file."""
from typing import Final, Optional
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_USER_AGENT: Final[str] = 'Udemate:v1.0.0 (by u/kemitche)'
DEFAULT_LIMIT: Final[int] = 500
MIN_LIMIT: Final[int] = 1
MAX_LIMIT: Final[int] = 1000

BOT_DEFAULTS: Final[dict[str, dict[str, int]]] = {
    'coursecouponz': {'retries': 3, 'threads': 2, 'timeout': 30},
    'coursetreat': {'retries': 3, 'threads': 2, 'timeout': 30},
    'easylearn': {'retries': 3, 'threads': 10, 'timeout': 30},
    'freewebcart': {'retries': 3, 'threads': 2, 'timeout': 30},
    'idc': {'retries': 3, 'threads': 25, 'timeout': 30},
    'inventhigh': {'retries': 3, 'threads': 2, 'timeout': 30},
    'line51': {'retries': 3, 'threads': 2, 'timeout': 30},
    'webhelperapp': {'retries': 3, 'threads': 2, 'timeout': 30},
    'udemy': {'retries': 3, 'timeout': 10}
}

FORMATTED_DATE: Final[str] = datetime.today().strftime('%Y%m%d')


class Config(BaseSettings):
    """Encapsulate and validate configuration attributes loaded from .env."""
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      case_sensitive=False)
    reddit_client_id: str = Field(description='Reddit script client ID')
    reddit_client_secret: str = Field(
        description='Reddit script client secret')
    reddit_user_agent: str = Field(
        default=DEFAULT_USER_AGENT, description='Reddit script user agent')
    reddit_limit: int = Field(DEFAULT_LIMIT,
                              le=MAX_LIMIT,
                              ge=MIN_LIMIT,
                              description='Maximum number of posts parsed by Reddit script')
    reddit_password: str = Field(
        description='Password of Reddit account')
    reddit_username: str = Field(
        description='Username of Reddit account')

    user_data_dir: Optional[str] = Field(
        description='Path to Brave Browser user data directory'
    )

    coursecouponz_retries: Optional[int] = Field(
        description='Maximum number of retries for Course Couponz requests',
        default=BOT_DEFAULTS['coursecouponz']['retries']
    )
    coursecouponz_threads: Optional[int] = Field(
        description='Number of threads for Course Couponz requests',
        default=BOT_DEFAULTS['coursecouponz']['threads']
    )
    coursecouponz_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Course Couponz requests',
        default=BOT_DEFAULTS['coursecouponz']['timeout']
    )

    coursetreat_retries: Optional[int] = Field(
        description='Maximum number of retries for Course Treat requests',
        default=BOT_DEFAULTS['coursetreat']['retries']
    )
    coursetreat_threads: Optional[int] = Field(
        description='Number of threads for Course Treat requests',
        default=BOT_DEFAULTS['coursetreat']['threads']
    )
    coursetreat_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Course Treat requests',
        default=BOT_DEFAULTS['coursetreat']['timeout']
    )

    easylearn_retries: Optional[int] = Field(
        description='Maximum number of retries for Easy Learning requests',
        default=BOT_DEFAULTS['easylearn']['retries']
    )
    easylearn_threads: Optional[int] = Field(
        description='Number of threads for Easy Learning requests',
        default=BOT_DEFAULTS['easylearn']['threads']
    )
    easylearn_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Easy Learning requests and actions',
        default=BOT_DEFAULTS['easylearn']['timeout']
    )

    freewebcart_retries: Optional[int] = Field(
        description='Maximum number of retries for Freewebcart requests and actions',
        default=BOT_DEFAULTS['freewebcart']['retries']
    )
    freewebcart_threads: Optional[int] = Field(
        description='Number of threads for Freewebcart requests and actions',
        default=BOT_DEFAULTS['freewebcart']['threads']
    )
    freewebcart_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Freewebcart web requests and actions',
        default=BOT_DEFAULTS['freewebcart']['timeout']
    )

    idc_retries: Optional[int] = Field(
        description='Maximum number of retries for iDC requests',
        default=BOT_DEFAULTS['idc']['retries']
    )
    idc_threads: Optional[int] = Field(
        description='Number of threads for iDC requests',
        default=BOT_DEFAULTS['idc']['threads']
    )
    idc_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for iDC requests',
        default=BOT_DEFAULTS['idc']['timeout']
    )

    inventhigh_retries: Optional[int] = Field(
        description='Maximum number of retries for InventHigh requests and actions',
        default=BOT_DEFAULTS['inventhigh']['retries']
    )
    inventhigh_threads: Optional[int] = Field(
        description='Number of threads for InventHigh requests and actions',
        default=BOT_DEFAULTS['inventhigh']['threads']
    )
    inventhigh_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for InventHigh requests and actions',
        default=BOT_DEFAULTS['inventhigh']['timeout']
    )

    line51_retries: Optional[int] = Field(
        description='Maximum number of retries for Line51 requests and actions',
        default=BOT_DEFAULTS['line51']['retries']
    )
    line51_threads: Optional[int] = Field(
        description='Number of threads for Line51 requests and actions',
        default=2
    )
    line51_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Line51 requests and actions',
        default=BOT_DEFAULTS['line51']['timeout']
    )

    webhelperapp_retries: Optional[int] = Field(
        description='Maximum number of retries for WebHelperApp requests and actions',
        default=BOT_DEFAULTS['webhelperapp']['retries']
    )
    webhelperapp_threads: Optional[int] = Field(
        description='Number of threads for WebHelperApp requests and actions',
        default=BOT_DEFAULTS['webhelperapp']['threads']
    )
    webhelperapp_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for WebHelperApp requests and actions',
        default=BOT_DEFAULTS['webhelperapp']['timeout']
    )

    udemy_email: Optional[str] = Field(
        description='Email address for Udemy account',
        default=None
    )
    udemy_retries: Optional[int] = Field(
        description='Maximum number of retries for web actions such as enrollments',
        default=BOT_DEFAULTS['udemy']['retries']
    )
    udemy_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for web actions such as enrollments',
        default=BOT_DEFAULTS['udemy']['timeout']
    )

    gotify_base_url: Optional[str] = Field(
        description='Base URL of Gotify server',
        default=None
    )
    gotify_app_token: Optional[str] = Field(
        description='Application token for Gotify notifications',
        default=None
    )


class BaseConfig(BaseModel):
    """Encapsulate and validate base configuration attributes."""
    retries: int
    timeout: int


class BotConfig(BaseConfig):
    """Encapsulate and validate bot configuration attributes."""


class SpiderConfig(BaseConfig):
    """Encapsulate and validate spider configuration attributes."""
    threads: int
