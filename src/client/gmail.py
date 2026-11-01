"""Gmail API client setup and message retrieval."""
import re
import base64
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config.settings import BASE_DIR


class GmailClient:
    """Gmail API client for authentication and service creation."""

    def __init__(self, client_secret: Path) -> None:
        if not Path(BASE_DIR / 'sso').exists():
            Path(BASE_DIR / 'sso').mkdir(parents=True, exist_ok=True)
        self.client_secret = client_secret
        self.credentials_file = BASE_DIR / 'sso' / 'credentials.json'
        self.scopes = ['https://www.googleapis.com/auth/gmail.readonly']

    def setup_service(self):
        """Return Gmail API service object."""
        credentials: Credentials | None = None
        if (BASE_DIR / 'sso' / 'token.json').exists():
            credentials = Credentials.from_authorized_user_file(
                BASE_DIR / 'sso' / 'token.json', self.scopes
            )
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret, self.scopes
                )
                credentials = flow.run_local_server(port=0)
            with open(self.credentials_file, 'w', encoding='utf-8') as token:
                token.write(credentials.to_json())
        service = build('gmail', 'v1', credentials=credentials)
        return service

    def get_verification_code(self) -> str | None:
        """Return Udemy verification code from last email."""
        service = self.setup_service()
        results = service.users().messages().list(
            userId='me',
            q='from:udemy'
        ).execute()
        messages = results.get('messages', [])
        for msg in messages[:5]:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            for part in msg_data['payload'].get('parts', []):
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(
                        part['body']['data']
                    ).decode()
                    match = re.search(r'\d{6}', body)
                    if match:
                        return match.group()
        return None
