"""Improve performance by relying on cached Udemy links on startup."""
import json
from pathlib import Path

from utils.logger import setup_logging
from utils.config import FORMATTED_DATE


class Cache:
    """Read and write cached middleman and Udemy links to JSON files."""

    def __init__(self) -> None:
        self.json_dir = Path(__file__).parent.parent.parent / \
            'data' / FORMATTED_DATE / 'json'
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging()
        self.urls = {}

    def read_json(self, filename: str) -> bool:
        """Parse cached middleman and Udemy links with coupons from JSON files."""
        file_path: Path = self.json_dir / filename
        if file_path.exists():
            with file_path.open('r', encoding='utf-8') as f:
                self.urls[filename[:-5]] = list(json.load(f))
            if self.urls[filename[:-5]]:
                self.logger.info('Read %d links from %s.',
                                 len(self.urls[filename[:-5]]), filename[:-5])
            return True
        self.logger.info('No links in JSON cache for %s.', filename[:-5])
        return False

    def write_json(self, *, filename: str, data: list[str]) -> None:
        """Write output to JSON file in 'json' directory within 'data' directory."""
        file_path: Path = self.json_dir / filename
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(
                data, f,
                ensure_ascii=False, indent=4
            )
            self.logger.info('Successfully written data to %s.', file_path)

    def delete_json(self, filename: str) -> None:
        """Clear JSON file in 'json' directory within 'data' directory."""
        file_path: Path = self.json_dir / filename
        file_path.unlink(missing_ok=True)
        self.logger.info('Deleted %s.', filename[:-5])

    def read_jsonl(self, filename: str) -> list[str]:
        """Return a list of processed Udemy links from 'udemy.jsonl' file."""
        file_path: Path = self.json_dir / filename
        if file_path.exists():
            with file_path.open('r', encoding='utf-8') as f:
                return [json.loads(line) for line in f]
        return []

    def append_jsonl(self, *, filename: str, url: str) -> None:
        """Append Udemy link to JSONL file in 'json' directory within 'data' directory."""
        file_path: Path = self.json_dir / filename
        with file_path.open(mode='a', encoding='utf-8') as f:
            json.dump(url, f, ensure_ascii=False)
            f.write('\n')
        self.logger.info('Successfully appended %s to %s.', url, file_path)
