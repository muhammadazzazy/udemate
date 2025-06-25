#!/usr/bin/env python

"""
Unlock Udemy courses based on links posted on various middlemen websites.
"""
import sys
from logging import Logger

from cli.controller import Controller
from utils.logger import setup_logging


def main() -> None:
    """
    Instantiate and run CLI controller.
    """
    try:
        logger: Logger = setup_logging()
        controller: Controller = Controller()
        logger.info('Udemate: Your Automation Companion for Udemy 🤖 📚')
        controller.run()
    except ValueError as e:
        logger.exception(e)
        sys.exit()
    except KeyboardInterrupt:
        logger.exception('Interrupt signal (SIGINT) triggered! Exiting...')
        sys.exit()


if __name__ == '__main__':
    main()
