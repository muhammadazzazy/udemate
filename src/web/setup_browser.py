"""Manage Selenium WebDriver for scraping links and automating course enrollment."""
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config import Config


def launch_brave(*, user_data_dir: str, profile_dir: str, port: int) -> None:
    """
    Launch Brave Browser.
    """
    subprocess.run([
        "brave-browser",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile_dir}",
    ], check=True)

    time.sleep(3)


def setup_brave(headless: bool):
    """
    Return WebDriver for Brave Browser using a specific debugger address.
    """
    config: Config = Config()
    launch_brave(user_data_dir=config.user_data_dir,
                 profile_dir=config.profile_dir, port=config.port)
    options = Options()
    options.add_experimental_option(
        "debuggerAddress", f"127.0.0.1:{config.port}")
    if headless:
        options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver
