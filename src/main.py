#!/usr/bin/env python

"""
Unlock Udemy courses based on links posted on various middlemen websites.
"""
from argparse import ArgumentParser
from logging import Logger

from cli.udemate import Udemate
from utils.logger import setup_logging


def main() -> None:
    """Parse command-line arguments for mode of automation and run Udemate."""
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--mode",
                        choices=["headless", "gui", "hybrid"],
                        default="hybrid")
    args = parser.parse_args()
    logger: Logger = setup_logging()
    udemate: Udemate = Udemate()
    logger.info('Starting Udemate...')
    if args.mode in ('headless', 'hybrid'):
        udemate.scrape()
    if args.mode in ('hybrid', 'gui'):
        udemate.autoenroll()


if __name__ == '__main__':
    main()
