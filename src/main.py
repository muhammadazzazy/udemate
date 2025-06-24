#!/usr/bin/env python

"""
Unlock Udemy courses based on links posted on various middlemen websites.
"""
import sys


from cli.controller import Controller


def main() -> None:
    """
    Instantiate and run CLI controller.
    """
    try:
        controller: Controller = Controller()
        controller.run()
    except ValueError as e:
        print(e)
        sys.exit()
    except KeyboardInterrupt:
        print('Interrupt signal (SIGINT) triggered! Exiting...')
        sys.exit()


if __name__ == '__main__':
    main()
