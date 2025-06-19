"""Load environment variables from a .env file and get refresh token for Reddit bot."""
import os
import random
import socket
import sys

import praw
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


def get_refresh_token(env_vars: dict[str, str]) -> str:
    """Return refresh token."""
    reddit: praw.reddit.Reddit = praw.Reddit(
        client_id=env_vars['CLIENT_ID'],
        client_secret=env_vars['CLIENT_SECRET'],
        redirect_uri='http://localhost:8080',
        user_agent=env_vars['USER_AGENT']
    )
    state: str = str(random.randint(0, 65000))
    url: str = reddit.auth.url(
        duration='permanent', scopes=['read'], state=state)
    print(f'Open this url in your browser: {url}')

    client: socket.socket = receive_connection()
    data: str = client.recv(1024).decode('utf-8')
    param_tokens: list[str] = data.split(' ', 2)[1].split('?', 1)[1].split('&')
    params: dict[str, str] = dict([token.split('=') for token in param_tokens])
    if state != params['state']:
        send_message(
            client,
            f"State mismatch. Expected: {state} Received: {params['state']}",
        )
        raise ValueError("OAuth state mismatch.")
    if 'error' in params:
        send_message(client, params['error'])
        raise ValueError(f"OAuth error: {params['error']}")
    refresh_token: str = reddit.auth.authorize(params['code'])
    send_message(client, f'Refresh token: {refresh_token}')
    return refresh_token


def receive_connection() -> socket.socket:
    """
    Wait for and then return a connected socket.

    Open a TCP connection on port 8080 and wait for a single client.
    """
    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client: socket.socket = server.accept()[0]
    server.close()
    return client


def send_message(client, message) -> None:
    """Send message to client and close the connection."""
    client.send(f'HTTP/1.1 200 OK\r\n\r\n{message}'.encode())
    client.close()


def main() -> None:
    """
    Coordinate program execution.

    Invoke a function to load environment variables and get refresh token.
    """
    try:
        env_vars: dict[str, str] = get_config()
        print(f'{env_vars=}')
        refresh_token: str = get_refresh_token(env_vars)
        print(f'{refresh_token=}')
    except ValueError as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
