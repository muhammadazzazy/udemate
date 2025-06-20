"""
Load environment variables from a .env file, get refresh token for Reddit bot,
get Udemy links with coupons, and generate JSON files for submissions grouped by hostname.
"""
import json
import os
import random
import socket
import sys
from pathlib import Path
from typing import Final
from urllib.parse import urlparse

import praw
import requests
from dotenv import load_dotenv
from praw.models.reddit.submission import Submission
from praw.models.reddit.subreddit import Subreddit
from praw.reddit import Reddit


SUBREDDIT_NAME: Final[str] = 'udemyfreebies'


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
    reddit: Reddit = praw.Reddit(
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


def send_message(client: socket.socket, message: str) -> None:
    """Send message to client and close the connection."""
    client.send(f'HTTP/1.1 200 OK\r\n\r\n{message}'.encode())
    client.close()


def get_submissions(subreddit) -> list[Submission]:
    """Return list of Reddit submissions."""
    submissions: list[Submission] = []
    for submission in subreddit.new(limit=100):
        submissions.append(submission)
    return submissions


def get_hostnames(submissions: list[Submission]) -> set[str]:
    """Return set of hostnames."""
    hostnames: set[str] = set()
    for submission in submissions:
        domain: str = urlparse(submission.url).netloc
        parts: list[str] = domain.split('.')
        if 'reddit' not in domain and domain:
            if domain.startswith('www.'):
                hostname: str = parts[1]
            else:
                hostname: str = parts[0]
            hostnames.add(hostname)
    return hostnames


def get_udemy_urls(submissions: list[Submission]) -> list[str]:
    """Return list of Udemy links with coupons for IDC."""
    udemy_urls: list[str] = []
    for submission in submissions:
        if 'idownloadcoupon' in submission.url:
            response = requests.get(
                submission.url, allow_redirects=True, timeout=10)
            url: str = response.url
            if 'udemy.com' in url:
                udemy_url: str = url
                udemy_urls.append(udemy_url)

    return udemy_urls


def format_data(*, submissions: list[Submission],
                hostnames: set[str]) -> list[dict[str, str]]:
    """Format output data."""
    data: dict[str, list[dict[str, str]]] = {
        hostname: [] for hostname in hostnames}
    for submission in submissions:
        for hostname in hostnames:
            if hostname in submission.url:
                data[hostname].append({
                    'title': submission.title,
                    'url': submission.url
                })
    return data


def write_json(*, hostnames: set[str], data: dict[str, list[dict[str, str]]]) -> None:
    """Write output to JSON files in a 'data' directory inside the root directory."""
    data_dir: Path = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)

    for hostname in hostnames:
        file_path: Path = data_dir / f'{hostname}.json'
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data[hostname], f, ensure_ascii=False, indent=4)
        print(f'Successfully written data to {file_path}.')


def main() -> None:
    """
    Coordinate program execution.

    Invoke functions to load environment variables, get refresh token,
    get list of submissions, get set of hostnames, format data,
    get Udemy links with coupons, and write formatted data to JSON files grouped by hostname.
    """
    try:
        env_vars: dict[str, str] = get_config()
        print(f'{env_vars=}')
        refresh_token: str = get_refresh_token(env_vars)
        print(f'{refresh_token=}')
        reddit: Reddit = praw.Reddit(
            client_id=env_vars['CLIENT_ID'],
            client_secret=env_vars['CLIENT_SECRET'],
            user_agent=env_vars['USER_AGENT'],
            refresh_token=refresh_token
        )
        subreddit: Subreddit = reddit.subreddit(SUBREDDIT_NAME)
        submissions: list[Submission] = get_submissions(subreddit)
        hostnames: set[str] = get_hostnames(submissions)
        print(f'{hostnames=}')
        udemy_urls: list[str] = get_udemy_urls(submissions)
        print(f'{udemy_urls=}')
        data: dict[str, list[dict[str, str]]] = format_data(
            submissions=submissions, hostnames=hostnames)
        write_json(hostnames=hostnames, data=data)
    except ValueError as e:
        print(e)
        sys.exit()


if __name__ == '__main__':
    main()
