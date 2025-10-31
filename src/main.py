#!/usr/bin/env python

"""Autoenroll into free Udemy courses based on links posted on various middlemen websites."""
from argparse import ArgumentParser, Namespace
from logging import Logger
from pydantic_settings import BaseSettings

from cli.udemate import Udemate
from utils.config import Config
from utils.logger import setup_logging


def parse_arguments() -> Namespace:
    """Parse arguments passed via the CLI."""
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        '--mode',
        choices=['headless', 'gui', 'hybrid'],
        default='hybrid'
    )
    parser.add_argument(
        '--user-data-dir',
        type=str,
        default=None
    )
    parser.add_argument(
        '--retries',
        type=int,
        default=None
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=None
    )
    return parser.parse_args()


def override_env_vars(args: Namespace) -> BaseSettings:
    """Override environment variables with command-line arguments."""
    cli_overrides: dict[str, int | str | None] = {
        k: v for k, v in vars(args).items() if v is not None
    }
    config: Config = Config()
    settings: BaseSettings = config.model_copy(update=cli_overrides)
    return settings


def main() -> None:
    """Configure and run the automation tool."""
    logger: Logger = setup_logging()
    try:
        args: Namespace = parse_arguments()
        settings: BaseSettings = override_env_vars(args)
        udemate: Udemate = Udemate(
            config=settings,
            logger=logger
        )
        udemate.run(args.mode)
    except KeyboardInterrupt:
        logger.info('Exiting...')


if __name__ == '__main__':
    main()
