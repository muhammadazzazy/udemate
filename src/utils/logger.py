"""Setup Udemate logger to display stdout and write messages to log files."""

import logging
from logging import FileHandler, Formatter, Logger, StreamHandler
from pathlib import Path

from utils.config import FORMATTED_DATE


def setup_logging() -> logging.Logger:
    """Configure and return logger for Udemate."""
    logger: Logger = logging.getLogger('udemate')
    logs_dir = Path(__file__).resolve().parents[2] / 'logs' / FORMATTED_DATE
    logs_dir.mkdir(parents=True, exist_ok=True)
    if not logger.hasHandlers():
        file_handler: FileHandler = logging.FileHandler(
            logs_dir / 'udemate.log')
        stream_handler: StreamHandler = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
        formatter: Formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger
