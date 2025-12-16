"""Configuration models for bot and spider settings."""
from pydantic import BaseModel


class BaseConfig(BaseModel):
    """Encapsulate and validate base configuration attributes."""
    retries: int
    timeout: int


class BotConfig(BaseConfig):
    """Encapsulate and validate bot configuration attributes."""


class SpiderConfig(BaseConfig):
    """Encapsulate and validate spider configuration attributes."""
    threads: int
