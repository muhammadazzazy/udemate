"""Collect Freewebcart links from the Telegram channel @udemylive."""
import re
from logging import Logger

from telethon import TelegramClient


class TelegramBot:
    """Parse Freewebcart links from the Telegram channel @udemylive."""

    def __init__(self, *, name: str, api_id: int, api_hash: str, logger: Logger) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(name, api_id, api_hash)
        self.logger = logger

    async def fetch_deelcart_replies(self) -> list:
        """Fetch the latest messages from the Telegram channel."""
        deelcart_replies: list = []
        async for message in self.client.iter_messages('udemylive', limit=5):
            async for reply in self.client.iter_messages(
                'udemylive',
                reply_to=message.id,
                limit=100,
            ):
                self.logger.info('Reply %s: %s', reply.id, reply.text)
                deelcart_replies.append(reply)

        return deelcart_replies

    def extract_deelcart_links(self, replies: list) -> list[str]:
        """Extract Deelcart links from the messages."""
        deelcart_links: list[str] = []
        for reply in replies:
            if reply is not None:
                for link in re.findall(
                    r'https://deelcart\.com/course/[^\s)]+',
                    reply.text or '',
                ):
                    if link not in deelcart_links:
                        deelcart_links.append(link)
                        self.logger.info('Found Deelcart link: %s', link)
        return deelcart_links

    def run(self) -> list[str]:
        """Run the Telegram bot."""
        with self.client:
            deelcart_replies = self.client.loop.run_until_complete(
                self.fetch_deelcart_replies())
            deelcart_links = self.extract_deelcart_links(deelcart_replies)
            return deelcart_links
