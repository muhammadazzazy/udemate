"""Configure Udemate based on environment variables in .env file."""
from typing import Final, Optional
from datetime import datetime

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_USER_AGENT: Final[str] = 'Udemate:v1.0.0 (by u/kemitche)'
DEFAULT_LIMIT: Final[int] = 500
MIN_LIMIT: Final[int] = 1
MAX_LIMIT: Final[int] = 1000


DEFAULT_COURSECOUPONZ_TIMEOUT: Final[int] = 30
DEFAULT_COURSECOUPONZ_RETRIES: Final[int] = 3

DEFAULT_COURSETREAT_RETRIES: Final[int] = 3
DEFAULT_COURSETREAT_TIMEOUT: Final[int] = 30

DEFAULT_EASYLEARN_TIMEOUT: Final[int] = 30
DEFAULT_EASYLEARN_RETRIES: Final[int] = 3

DEFAULT_FREEWEBCART_TIMEOUT: Final[int] = 30
DEFAULT_FREEWEBCART_RETRIES: Final[int] = 3

DEFAULT_IDC_TIMEOUT: Final[int] = 30
DEFAULT_IDC_RETRIES: Final[int] = 3

DEFAULT_INVENTHIGH_TIMEOUT: Final[int] = 30
DEFAULT_INVENTHIGH_RETRIES: Final[int] = 3

DEFAULT_LINE51_TIMEOUT: Final[int] = 30
DEFAULT_LINE51_RETRIES: Final[int] = 3

DEFAULT_WEBHELPERAPP_TIMEOUT: Final[int] = 30
DEFAULT_WEBHELPERAPP_RETRIES: Final[int] = 3

DEFAULT_UDEMY_TIMEOUT: Final[int] = 10
DEFAULT_UDEMY_RETRIES: Final[int] = 3

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
        default=DEFAULT_COURSECOUPONZ_RETRIES
    )
    coursecouponz_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Course Couponz requests',
        default=DEFAULT_COURSECOUPONZ_TIMEOUT
    )

    coursetreat_retries: Optional[int] = Field(
        description='Maximum number of retries for Course Treat requests',
        default=DEFAULT_COURSETREAT_RETRIES
    )
    coursetreat_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Course Treat requests',
        default=DEFAULT_COURSETREAT_TIMEOUT
    )

    easylearn_retries: Optional[int] = Field(
        description='Maximum number of retries for Easy Learning requests',
        default=DEFAULT_EASYLEARN_RETRIES
    )
    easylearn_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Easy Learning requests',
        default=DEFAULT_EASYLEARN_TIMEOUT
    )

    freewebcart_retries: Optional[int] = Field(
        description='Maximum number of retries for Freewebcart requests and actions',
        default=DEFAULT_FREEWEBCART_RETRIES
    )
    freewebcart_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Freewebcart web requests and actions',
        default=DEFAULT_FREEWEBCART_TIMEOUT
    )

    idc_retries: Optional[int] = Field(
        description='Maximum number of retries for iDC requests',
        default=DEFAULT_IDC_RETRIES
    )
    idc_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for iDC requests',
        default=DEFAULT_IDC_TIMEOUT
    )

    inventhigh_retries: Optional[int] = Field(
        description='Maximum number of retries for InventHigh requests and actions',
        default=DEFAULT_INVENTHIGH_RETRIES
    )
    inventhigh_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for InventHigh requests and actions',
        default=DEFAULT_INVENTHIGH_TIMEOUT
    )

    line51_retries: Optional[int] = Field(
        description='Maximum number of retries for Line51 requests and actions',
        default=DEFAULT_LINE51_RETRIES
    )
    line51_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for Line51 requests and actions',
        default=DEFAULT_LINE51_TIMEOUT
    )

    webhelperapp_retries: Optional[int] = Field(
        description='Maximum number of retries for WebHelperApp requests and actions',
        default=DEFAULT_WEBHELPERAPP_RETRIES
    )
    webhelperapp_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for WebHelperApp requests and actions',
        default=DEFAULT_WEBHELPERAPP_TIMEOUT
    )

    udemy_retries: Optional[int] = Field(
        description='Maximum number of retries for web actions such as enrollments',
        default=DEFAULT_UDEMY_RETRIES
    )
    udemy_timeout: Optional[int] = Field(
        description='Timeout (in seconds) for web actions such as enrollments',
        default=DEFAULT_UDEMY_TIMEOUT
    )
