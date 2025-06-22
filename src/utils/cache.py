"""Improve performance by relying on cached Udemy links on startup."""
import json
from pathlib import Path


class Cache:
    """Read and write cached Udemy links to JSON files."""

    def __init__(self) -> None:
        self.data_dir: Path = Path(__file__).parent.parent.parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.udemy_urls: set[str] = set()

    def read(self) -> None:
        """Parse cached Udemy links with coupons from JSON files."""
        file_path: Path = self.data_dir / 'udemy.json'
        if file_path.exists():
            with file_path.open('r', encoding='utf-8') as f:
                self.udemy_urls = set(json.load(f))

    def write(self, data: set[str]) -> None:
        """Write output to JSON file in a 'data' directory inside root directory."""
        file_path: Path = self.data_dir / 'udemy.json'
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(list(data), f,
                      ensure_ascii=False, indent=4)
        print(f'Successfully written data to {file_path}.')
