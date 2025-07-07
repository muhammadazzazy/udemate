"""Improve performance by relying on cached Udemy links on startup."""
import json
from pathlib import Path

from utils.logger import setup_logging
from utils.config import FORMATTED_DATE


class Cache:
    """Read and write cached middleman and Udemy links to JSON files."""

    def __init__(self) -> None:
        self.json_dir: Path = Path(
            __file__).parent.parent.parent / 'data' / FORMATTED_DATE / 'json'
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging()
        self.urls: dict[str, set[str]] = {}

    def read_json(self, filename: str, brand_name: str) -> bool:
        """Parse cached middleman and Udemy links with coupons from JSON files."""
        file_path: Path = self.json_dir / filename
        if file_path.exists():
            with file_path.open('r', encoding='utf-8') as f:
                self.urls[filename[:-5]] = set(json.load(f))
            if self.urls[filename[:-5]]:
                self.logger.info('Read %d %s links from JSON cache.',
                                 len(self.urls[filename[:-5]]), brand_name)
            return True
        self.logger.info('No %s links in JSON cache.', brand_name)
        return False

    def write_json(self, *, filename: str, data: set[str]) -> None:
        """Write output to JSON file in 'json' directory within 'data' directory."""
        file_path: Path = self.json_dir / filename
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(list(data), f,
                      ensure_ascii=False, indent=4)
            self.logger.info('Successfully written data to %s.', file_path)

    def delete_json(self, filename: str, brand_name: str) -> None:
        """Clear JSON file in 'json' directory within 'data' directory"""
        file_path: Path = self.json_dir / filename
        file_path.unlink(missing_ok=True)
        self.logger.info('Cleared cache for %s', brand_name)
