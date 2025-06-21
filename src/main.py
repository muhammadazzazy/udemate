#!/usr/bin/env python

"""
Load environment variables from a .env file, get refresh token for Reddit bot,
get Udemy links with coupons, and generate JSON files for submissions grouped by hostname.
"""
import json
import os

import sys
from pathlib import Path
from typing import Final
from urllib.parse import urlparse

import praw
import requests
from dotenv import load_dotenv
from praw.models.reddit.submission import Submission
from praw.models.reddit.subreddit import Subreddit
from praw.reddit import Reddit
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from get_refresh_token import get_refresh_token

DEFAULT_LIMIT: Final[int] = 500
MAX_LIMIT: Final[int] = 1000
SUBREDDIT_NAME: Final[str] = 'udemyfreebies'


def get_config() -> dict[str, str]:
    """
    Return dictionary of parsed environment variables.

    Raise:
        ValueError: If an environment variable is missing.
    """
    load_dotenv()
    env_vars: dict[str, str] = {
        'CLIENT_ID': os.environ.get('CLIENT_ID'),
        'CLIENT_SECRET': os.environ.get('CLIENT_SECRET'),
        'USER_AGENT': os.environ.get('USER_AGENT'),
        'LIMIT': int(os.environ.get('LIMIT', DEFAULT_LIMIT)),
        'DEBUGGER_PORT': os.environ.get('DEBUGGER_PORT', '9222'),
        'BINARY_LOCATION': os.environ.get('BINARY_LOCATION', '/usr/bin/google-chrome')
    }
    missing: list[str] = [
        env_var[0] for env_var in env_vars.items() if not env_var[1]]
    if not all(env_vars.values()):
        raise ValueError(
            f'Missing environment variable(s): {', '.join(missing)}')
    if env_vars['LIMIT'] > MAX_LIMIT:
        print(f"Max value for 'LIMIT' is {MAX_LIMIT}...")
        env_vars['LIMIT'] = MAX_LIMIT
    return env_vars


def read_cache(data_dir: Path) -> dict[str, set[str]]:
    """Return cached Udemy links with coupons from JSON files."""
    file_paths = []
    hostnames = []
    for filename in os.listdir(data_dir):
        file_path = data_dir / filename
        if os.path.isfile(file_path) and filename.lower().endswith('.json'):
            file_paths.append(file_path)
            hostnames.append(filename[:filename.find('.json')])
    cached_urls: dict[str, set[str]] = {
        hostname: set() for hostname in hostnames
    }
    for (file_path, hostname) in zip(file_paths, hostnames):
        with file_path.open('r', encoding='utf-8') as f:
            cached_urls[hostname] = set(json.load(f))
    return cached_urls


def get_submissions(*, subreddit: Subreddit, limit: int) -> list[Submission]:
    """Return list of Reddit submissions."""
    submissions: list[Submission] = []
    for submission in subreddit.new(limit=limit):
        submissions.append(submission)
    return submissions


def get_hostnames(submissions: list[Submission]) -> set[str]:
    """Return set of hostnames."""
    hostnames: set[str] = set()
    for submission in submissions:
        domain: str = urlparse(submission.url).netloc
        parts: list[str] = domain.split('.')
        if 'reddit' not in domain and domain:
            if domain.startswith('www.'):
                hostname: str = parts[1]
            else:
                hostname: str = parts[0]
            hostnames.add(hostname)
    return hostnames


def fetch_urls(submissions: list[Submission], hostnames: list[str]) -> dict[str, set[str]]:
    """Return mapping between hostnames and submission links."""
    urls: dict[str, set[str]] = {
        hostname: set() for hostname in hostnames
    }
    for submission in submissions:
        for hostname in hostnames:
            if hostname in submission.url:
                urls[hostname].add(submission.url)
    return urls


def setup_chromium_browser(debugger_address: str, binary_location: str) -> WebDriver:
    """Return Chrome WebDriver connected to a Chromium-based browser."""
    print(f'Connecting to Chromium-based browser at {debugger_address}...')
    options = Options()
    options.debugger_address = debugger_address
    options.binary_location = binary_location
    driver = webdriver.Chrome(options=options)
    print('Connected!')
    return driver


def get_idc_coupons(driver: WebDriver, idc_urls: list[str]) -> set[str]:
    """Return set of Udemy links from IDC links."""
    udemy_urls: set[str] = set()
    for idc_url in idc_urls:
        try:
            response = requests.get(idc_url, allow_redirects=True, timeout=10)
        except RequestException as e:
            print(e)
            continue
        if 'udemy.com' in response.url:
            udemy_urls.add(response.url)
            continue
        try:
            driver.get(idc_url)
            wait = WebDriverWait(driver, 15)
            form = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "form.cart")))
            action_url = form.get_attribute("action")
            response = requests.get(action_url, allow_redirects=True,
                                    timeout=15)
            udemy_urls.add(response.url)
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
            print(e)
            continue
    return udemy_urls


def auto_enroll(*, driver: WebDriver, udemy_urls: set[str]) -> None:
    """Automates Udemy course enrollment."""
    for udemy_url in udemy_urls:
        driver.get(udemy_url)
        print("Udemy page title:", driver.title)
        try:
            wait = WebDriverWait(driver, 30)
            buttons = wait.until(lambda d: d.find_elements(
                By.XPATH,
                "//button[@data-purpose='buy-this-course-button' and contains(., 'Enroll')]",
            ))

            enroll_button = next(
                (b for b in buttons if b.is_displayed() and b.is_enabled()), None)

            print(f"Clicking visible enroll button: {enroll_button.text}")
            enroll_button.click()
            print("Clicked first enroll button!")
            enroll_button = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="udemy"]/div[1]/div[2]/div/div/div/aside/div/div/div[2]/div[2]/button[1]'
            )))
            print("Clicked final enroll button!")
            enroll_button.click()
        except (TimeoutException, AttributeError):
            print(f'Enroll button not found for {driver.title}. Skipping...')
            continue


def write_json(data_dir: Path, data: dict[str, set[str]]) -> None:
    """Write output to JSON files in a 'data' directory inside the root directory."""
    for hostname in data.keys():
        file_path: Path = data_dir / f'{hostname}.json'
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(list(data[hostname]), f,
                      ensure_ascii=False, indent=4)
        print(f'Successfully written data to {file_path}.')


def run() -> None:
    """
    Invoke functions to load environment variables, get refresh token,
    get list of submissions, get set of hostnames, get Udemy links with coupons,
    autoenroll into free courses, format data,
    and write formatted data to JSON files grouped by hostname.
    """
    data_dir: Path = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    env_vars: dict[str, str] = get_config()
    cached_urls: dict[str, set[str]] = read_cache(data_dir)

    driver: WebDriver = setup_chromium_browser(f'127.0.0.1:{env_vars['DEBUGGER_PORT']}',
                                               env_vars['BINARY_LOCATION'])

    if cached_urls:
        auto_enroll(driver=driver, udemy_urls=cached_urls['idownloadcoupon'])

    refresh_token: str = get_refresh_token(env_vars)

    reddit: Reddit = praw.Reddit(
        client_id=env_vars['CLIENT_ID'],
        client_secret=env_vars['CLIENT_SECRET'],
        user_agent=env_vars['USER_AGENT'],
        refresh_token=refresh_token
    )
    subreddit: Subreddit = reddit.subreddit(SUBREDDIT_NAME)

    submissions: list[Submission] = get_submissions(
        subreddit=subreddit, limit=env_vars['LIMIT'])

    hostnames: set[str] = get_hostnames(submissions)

    urls: dict[str, set[str]] = fetch_urls(
        submissions=submissions, hostnames=hostnames)

    idc_coupons: set[str] = get_idc_coupons(driver, urls['idownloadcoupon'])
    print(f'{idc_coupons=}')
    data: dict[str, set[str]] = {
        'idownloadcoupon': idc_coupons
    }
    write_json(data_dir=data_dir, data=data)


def main() -> None:
    """Coordinate program execution."""
    print('📚 Welcome to Udemy Unlocked! 🔐')
    try:
        run()
    except ValueError as e:
        print(e)
        sys.exit()
    except KeyboardInterrupt:
        print('Interrupt signal (SIGINT) triggered! Exiting...')
        sys.exit()


if __name__ == '__main__':
    main()
