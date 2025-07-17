#!/usr/bin/env python

"""Autoenroll into free Udemy courses based on links posted on various middlemen websites."""
from argparse import ArgumentParser
from logging import Logger

from cli.udemate import Udemate
from utils.logger import setup_logging


def main() -> None:
    """Parse command-line arguments for mode of automation and run Udemate accordingly."""
    try:
        parser: ArgumentParser = ArgumentParser()
        parser.add_argument("--mode",
                            choices=["headless", "gui", "hybrid"],
                            default="hybrid")
        args = parser.parse_args()
        logger: Logger = setup_logging()
        udemate: Udemate = Udemate()
        logger.info('Starting Udemate in %s mode...', args.mode)
        if args.mode in ('headless', 'hybrid'):
            udemate.scrape()
        if args.mode in ('hybrid', 'gui'):
            udemate.autoenroll()
    except KeyboardInterrupt:
        logger.info('Exiting...')


if __name__ == '__main__':
    main()
