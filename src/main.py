"""Load environment variables from a .env file."""
import os
import sys

from dotenv import load_dotenv


def get_config() -> dict[str, str]:
    """
    Return dictionary of parsed environment variables.

    Raise:
        ValueError: If an environment variable is missing.
    """
    load_dotenv()
    env_vars: dict[str, str] = {
        'CLIENT_ID': os.environ.get('CLIENT_ID'),
        'CLIENT_SECRET': os.environ.get('CLIENT_SECRET'),
        'USER_AGENT': os.environ.get('USER_AGENT'),
    }
    missing: list[str] = [
        env_var[0] for env_var in env_vars.items() if not env_var[1]]
    print(f'{missing=}')
    if not all(env_vars.values()):
        raise ValueError(
            f'Missing environment variable(s): {', '.join(missing)}')
    return env_vars


def main() -> None:
    """
    Coordinate program execution.

    Invoke a function to load environment variables.
    """
    try:
        env_vars: dict[str, str] = get_config()
        print(f'{env_vars=}')
    except ValueError as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
