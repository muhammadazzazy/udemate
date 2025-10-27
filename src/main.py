#!/usr/bin/env python

"""Autoenroll into free Udemy courses based on links posted on various middlemen websites."""
from argparse import ArgumentParser, Namespace

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
        '--browser',
        choices=['brave', 'chrome'],
        default='brave'
    )
    parser.add_argument(
        '--retries',
        type=int,
        default=5
    )
    return parser.parse_args()


def main() -> None:
    """Parse command-line arguments for mode of automation and run Udemate accordingly."""
    logger = setup_logging()
    try:
        args: Namespace = parse_arguments()
        config: Config = Config()
        udemate: Udemate = Udemate(
            browser=args.browser,
            config=config,
            logger=logger,
            retries=args.retries
        )
        udemate.run(args)
    except KeyboardInterrupt:
        logger.info('Exiting...')


if __name__ == '__main__':
    main()
