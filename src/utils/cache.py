"""Improve performance by relying on cached Udemy links on startup."""
import json
from pathlib import Path

from utils.logger import setup_logging
from utils.config import FORMATTED_DATE


class Cache:
    """Read and write cached Udemy links to JSON files."""

    def __init__(self) -> None:
        self.json_dir: Path = Path(
            __file__).parent.parent.parent / 'data' / FORMATTED_DATE / 'json'
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging()
        self.udemy_urls: set[str] = set()

    def read_json(self) -> None:
        """Parse cached Udemy links with coupons from JSON files."""
        file_path: Path = self.json_dir / 'udemy.json'
        if file_path.exists():
            with file_path.open('r', encoding='utf-8') as f:
                self.udemy_urls = set(json.load(f))
        self.logger.info("Read %d Udemy links from cache.",
                         len(self.udemy_urls))

    def write_json(self, data: set[str]) -> None:
        """Write output to JSON file in a 'data' directory inside root directory."""
        file_path: Path = self.json_dir / 'udemy.json'
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(list(data), f,
                      ensure_ascii=False, indent=4)
            self.logger.info('Successfully written data to %s.', file_path)
