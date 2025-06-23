"""Manage Undetected ChromeDriver for scraping links and automating course enrollment."""
import undetected_chromedriver as uc


def setup_browser(user_data_dir: str, headless: bool):
    """Return Undetected ChromeDriver in headless mode."""
    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    else:
        options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    return driver
