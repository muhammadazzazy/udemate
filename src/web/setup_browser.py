"""Manage Undetected ChromeDriver for scraping links and automating course enrollment."""
import undetected_chromedriver as uc


def setup_browser(user_data_dir: str, headless: bool):
    """Return Undetected ChromeDriver in headless mode."""
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    if headless:
        options.add_argument("--headless")
    driver = uc.Chrome(options=options)
    return driver
