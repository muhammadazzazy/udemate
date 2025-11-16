"""Automatically enroll into free Udemy courses."""
import random
import time

import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from client.gotify import GotifyClient
from utils.cache import Cache
from utils.config import BotConfig
from utils.logger import setup_logging


class Udemy:
    """Autoenroll into free Udemy courses."""

    def __init__(self, *, driver: uc.Chrome, urls: list[str],
                 config: BotConfig, gotify: GotifyClient) -> None:
        self.cache = Cache()
        self.driver = driver
        self.logger = setup_logging()
        self.config = config
        self.urls = urls
        self.gotify = gotify
        self.patterns = {'paid': 'cart/success', 'free': 'cart/subscribe'}

    def confirm(self) -> bool:
        """Scan for final 'Enroll now' button and click on it."""
        xp: str = '//*[@id="udemy"]/div[1]/div[2]/div/div/div/aside/div/div/div[2]/div[2]/button[1]'
        for attempt in range(self.config.retries):
            try:
                wait: WebDriverWait = WebDriverWait(
                    self.driver, timeout=self.config.timeout)
                confirm_button: uc.WebElement = wait.until(EC.element_to_be_clickable((
                    By.XPATH,
                    xp
                )))
                confirm_button.click()
                time.sleep(random.uniform(2, 4))
                if self.patterns['paid'] in self.driver.current_url:
                    self.logger.info('Attempt %d/%d succeeded!',
                                     attempt+1,
                                     self.config.retries)
                    return True
                self.logger.warning('Attempt %d/%d failed.',
                                    attempt+1,
                                    self.config.retries)
            except WebDriverException as e:
                self.logger.error('Webdriver error: %r', e)
                continue
        return False

    def is_owned(self) -> bool:
        """Return a flag indicating whether a course is owned."""
        button_xpath: str = (
            "//button[(@data-purpose='buy-now-button' or @data-purpose='buy-this-course-button') and contains(., 'Go to course')]"
        )
        try:
            wait: WebDriverWait = WebDriverWait(
                self.driver, timeout=self.config.timeout)
            _buttons: list[uc.WebElement] = wait.until(lambda d: d.find_elements(
                By.XPATH,
                button_xpath,
            ))
            return True
        except WebDriverException:
            return False

    def is_paid(self) -> bool:
        """Return a flag whether course is paid."""
        button_xpath: str = (
            "//button[(@data-purpose='buy-now-button' or @data-purpose='buy-this-course-button') and contains(., 'Buy now')]"
        )
        try:
            wait: WebDriverWait = WebDriverWait(
                self.driver, timeout=self.config.timeout)
            _buttons: list[uc.WebElement] = wait.until(lambda d: d.find_elements(
                By.XPATH,
                button_xpath
            ))
            return True
        except WebDriverException:
            return False

    def enroll(self) -> bool:
        """Scan for first 'Enroll now' button and click on it."""
        button_xpath: str = (
            "//button[(@data-purpose='buy-now-button' or @data-purpose='buy-this-course-button') and contains(., 'Enroll now')]"
        )
        for attempt in range(self.config.retries):
            try:
                wait: WebDriverWait = WebDriverWait(
                    self.driver, timeout=self.config.timeout)
                buttons: list[uc.WebElement] = wait.until(lambda d: d.find_elements(
                    By.XPATH,
                    button_xpath
                ))
                enroll_button = next(
                    (b for b in buttons if b.is_displayed() and b.is_enabled()), None)
                enroll_button.click()
                self.logger.info('Attempt %d/%d succeeded!',
                                 attempt+1,
                                 self.config.retries)
                return True
            except WebDriverException:
                self.logger.warning('Attempt %d/%d failed.',
                                    attempt+1,
                                    self.config.retries)
                time.sleep(random.uniform(2, 4))
                continue

    def run(self) -> None:
        """Orchestrate automatic enrollment into Udemy courses."""
        self.logger.info('Udemy bot starting...')
        count: dict[str, int] = {'owned': 0, 'paid': 0, 'enroll': 0}
        for udemy_url in self.urls:
            self.logger.info('Visiting %s', udemy_url)
            self.driver.get(udemy_url)
            course_name: str = self.driver.title.removesuffix(' | Udemy')
            self.cache.append_jsonl(filename='udemy.jsonl', url=udemy_url)
            if self.is_owned():
                self.logger.info('%s is owned. Skipping...', course_name)
                count['owned'] += 1
            elif self.is_paid():
                self.logger.info('%s is paid. Skipping...', course_name)
                count['paid'] += 1
            elif self.enroll():
                self.logger.info('Enrolling into %s', course_name)
                if self.patterns['free'] in self.driver.current_url:
                    self.logger.info('Successfully enrolled into %s',
                                     course_name)
                    self.gotify.create_message(
                        title='Udemy Enrollment Successful',
                        message=f'Enrolled into {course_name}',
                    )
                    count['enroll'] += 1
                    continue
                if self.confirm():
                    self.logger.info('Successfully enrolled into %s.',
                                     course_name)
                    self.gotify.create_message(
                        title='Udemy Enrollment Successful',
                        message=f'Enrolled into {course_name}',
                    )
                    count['enroll'] += 1
                else:
                    self.logger.info('Failed to enroll into %s', course_name)
            else:
                self.logger.info('Course is unavailable. Skipping...')
        self.logger.info(
            'Encountered %d already owned courses.',
            count['owned']
        )
        self.logger.info(
            'Encountered %d paid courses.',
            count['paid']
        )
        self.logger.info(
            'Enrolled into %d free courses.',
            count['enroll']
        )
