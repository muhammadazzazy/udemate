#!/usr/bin/env python

"""
Unlock Udemy courses based on links posted on various middlemen websites.
"""
from logging import Logger

from cli.controller import Controller
from utils.logger import setup_logging


def main() -> None:
    """
    Instantiate and run CLI controller.
    """
    logger: Logger = setup_logging()
    controller: Controller = Controller()
    logger.info('Starting Udemate...')
    controller.run()


if __name__ == '__main__':
    main()
