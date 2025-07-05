#!/usr/bin/env python

"""
Unlock Udemy courses based on links posted on various middlemen websites.
"""
from argparse import ArgumentParser
from logging import Logger

from cli.udemate import Udemate
from utils.logger import setup_logging


def main() -> None:
    """
    Instantiate and run CLI controller.
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--mode",
                        choices=["headless", "non-headless", "hybrid"],
                        default="headless")
    args = parser.parse_args()
    logger: Logger = setup_logging()
    controller: Udemate = Udemate()
    logger.info('Starting Udemate...')
    controller.run(args)


if __name__ == '__main__':
    main()
