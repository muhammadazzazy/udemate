#!/usr/bin/env python

"""
Adapted from https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html.

Acquire a refresh token for setting up the Reddit client.
"""
import random
import socket

import praw
from praw.reddit import Reddit

from utils.config import Config


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


def get_refresh_token(config: Config) -> str:
    """Return refresh token."""
    reddit: Reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        redirect_uri='http://localhost:8080',
        user_agent=config.user_agent
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
