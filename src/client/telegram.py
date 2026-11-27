"""Collect intermediary links from Telegram channels."""
import re
from logging import Logger

from telethon import TelegramClient


class TelegramBot:
    """
    Parse Deelcart and InventHigh links 
    from the Telegram channels @udemylive and @udemyoffer, respectively.
    """

    def __init__(self, *, name: str, api_id: int, api_hash: str, logger: Logger) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(name, api_id, api_hash)
        self.logger = logger

    async def fetch_deelcart_replies(self) -> list:
        """Fetch the latest messages from the Telegram channel."""
        deelcart_replies: list = []
        async for message in self.client.iter_messages('udemylive', limit=5):
            self.logger.info('Processing message: %s', message.id)
            async for reply in self.client.iter_messages(
                'udemylive',
                reply_to=message.id,
                limit=100,
            ):
                self.logger.info('Processing reply: %s', reply.id)
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

    async def fetch_inventhigh_messages(self) -> list:
        """Fetch the latest messages from the Telegram channel @udemyoffer."""
        inventhigh_messages: list = []
        async for message in self.client.iter_messages('udemyoffer', limit=10):
            self.logger.info('Processing message: %s', message.id)
            inventhigh_messages.append(message)
        return inventhigh_messages

    def extract_inventhigh_links(self, messages: list) -> list[str]:
        """Extract InventHigh links from the messages."""
        inventhigh_links: list[str] = []
        for message in messages:
            if message is not None:
                for link in re.findall(
                    r'https://inventhigh\.net/udemy/[^\s)]+',
                    message.text or '',
                ):
                    if link not in inventhigh_links:
                        inventhigh_links.append(link)
                        self.logger.info('Found Inventhigh link: %s', link)
        return inventhigh_links

    def collect_intermediary_links(self) -> dict[str, list[str]]:
        """Return a dictionary containing Deelcart and InventHigh links."""
        intermediary_links: dict[str, list[str]] = {}
        with self.client:
            deelcart_replies: list = self.client.loop.run_until_complete(
                self.fetch_deelcart_replies())
            deelcart_links: list[str] = self.extract_deelcart_links(
                deelcart_replies)
            inventhigh_messages: list = self.client.loop.run_until_complete(
                self.fetch_inventhigh_messages())
            inventhigh_links: list[str] = self.extract_inventhigh_links(
                inventhigh_messages)
            intermediary_links: dict[str, list[str]] = {}
            intermediary_links['deelcart'] = deelcart_links
            intermediary_links['inventhigh'] = inventhigh_links
        return intermediary_links
