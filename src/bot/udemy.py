"""Automatically enroll into free Udemy courses."""
import random
import time

import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from client.gotify import GotifyClient
from config.bot import BotConfig
from utils.cache import Cache
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
        self.patterns = {'enroll': 'payment/checkout',
                         'confirm': 'cart/success', 'free': 'cart/subscribe'}

    def enter_email(self, wait: WebDriverWait, email: str) -> True:
        """Enter email address into login form."""
        for retry in range(self.config.retries):
            try:
                container = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".ud-compact-form-control-container")))
                container.click()
                email_input = wait.until(
                    EC.visibility_of_element_located((By.NAME, "email")))
                email_input.clear()
                email_input.send_keys(email)
                self.logger.info('Entered email address successfully.')
                return True
            except WebDriverException as e:
                self.logger.error(
                    'Error entering email address (attempt %d/%d): %s',
                    retry+1,
                    self.config.retries,
                    e
                )
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))
        return False

    def click_login_btn(self, wait: WebDriverWait) -> bool:
        """Click on the login button on Udemy homepage."""
        for retry in range(self.config.retries):
            try:
                login_button: uc.WebElement = wait.until(EC.element_to_be_clickable((
                    By.LINK_TEXT,
                    'Log in'
                )))
                login_button.click()
                return True
            except WebDriverException as e:
                self.logger.error(
                    'Error clicking login button (attempt %d/%d): %s',
                    retry+1,
                    self.config.retries,
                    e
                )
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout
                ))
        return False

    def click_continue_btn(self, wait: WebDriverWait) -> bool:
        """Click on the Continue button after entering email."""
        for retry in range(self.config.retries):
            try:
                continue_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//button[.//span[normalize-space()='Continue']]")
                    )
                )
                continue_btn.click()
                return True
            except WebDriverException as e:
                self.logger.error(
                    'Error clicking Continue button (attempt %d/%d): %s',
                    retry+1,
                    self.config.retries,
                    e
                )
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout
                ))
        return False

    def login(self, email: str) -> bool:
        """Log into Udemy account."""
        self.driver.get('https://www.udemy.com/')
        wait: WebDriverWait = WebDriverWait(
            self.driver, timeout=self.config.timeout)
        if not self.click_login_btn(wait):
            self.logger.error('Failed to click login button.')
            return False

        if not self.enter_email(wait, email):
            self.logger.error('Failed to enter email address.')
            return False

        if not self.click_continue_btn(wait):
            self.logger.error('Failed to click Continue button.')
            return False

        self.logger.info('Clicked Continue button successfully.')
        _user_input: str = input(
            'Please complete any additional login steps and press Enter to continue...'
        )
        return True

    def get_first_button(self, text: str) -> uc.WebElement | None:
        """Get the first enroll button that is clickable."""
        button_xpath: str = (
            "//button[(@data-purpose='buy-now-button' or @data-purpose='buy-this-course-button')"
            f" and (contains(., '{text}'))]"
        )
        wait: WebDriverWait = WebDriverWait(
            self.driver, timeout=self.config.timeout)
        buttons: list[uc.WebElement] = wait.until(lambda d: d.find_elements(
            By.XPATH,
            button_xpath
        ))
        button = next(
            (b for b in buttons if b.is_displayed() and b.is_enabled()), None)
        return button

    def get_second_button(self) -> uc.WebElement | None:
        """Get the second enroll button that is clickable."""
        xp: str = '//*[@id="udemy"]/div[1]/div[2]/div/div/div/aside/div/div/div[2]/div[2]/button[1]'
        wait: WebDriverWait = WebDriverWait(
            self.driver, timeout=self.config.timeout)
        confirm_button: uc.WebElement = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            xp
        )))
        return confirm_button

    def is_owned(self) -> bool:
        """Return a flag indicating whether a course is owned."""
        try:
            _button: uc.WebElement | None = self.get_first_button(
                text='Go to course')
            return True
        except WebDriverException:
            return False

    def is_paid(self) -> bool:
        """Return a flag whether course is paid."""
        try:
            _button: uc.WebElement = self.get_first_button(text='Buy now')
            return True
        except WebDriverException:
            return False

    def enroll(self) -> bool:
        """Scan for first 'Enroll now' button and click on it."""
        for attempt in range(self.config.retries):
            try:
                enroll_button: uc.WebElement = self.get_first_button(
                    text='Enroll now')
                enroll_button.click()
                wait: WebDriverWait = WebDriverWait(
                    self.driver, timeout=self.config.timeout)
                wait.until(
                    EC.url_contains(self.patterns['enroll'])
                )
                self.logger.info('Attempt %d/%d succeeded!',
                                 attempt+1,
                                 self.config.retries)
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))
                return True
            except WebDriverException:
                self.logger.warning('Attempt %d/%d failed.',
                                    attempt+1,
                                    self.config.retries)
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))
                continue
        return False

    def confirm(self) -> bool:
        """Scan for final 'Enroll now' button and click on it."""
        for attempt in range(self.config.retries):
            try:
                confirm_button: uc.WebElement = self.get_second_button()
                confirm_button.click()
                wait: WebDriverWait = WebDriverWait(
                    self.driver, timeout=self.config.timeout)
                wait.until(
                    EC.url_contains(self.patterns['confirm'])
                )
                self.logger.info('Attempt %d/%d succeeded!',
                                 attempt+1,
                                 self.config.retries)
                return True
            except WebDriverException:
                self.logger.warning('Attempt %d/%d failed.',
                                    attempt+1,
                                    self.config.retries)
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))
                continue
        return False

    def summarize_stats(self, courses: dict[str, list[str]]) -> None:
        """Summarize enrollment statistics."""
        self.logger.info(
            'Encountered %d already owned courses.',
            len(courses['owned'])
        )
        self.logger.info(
            'Encountered %d paid courses.',
            len(courses['paid'])
        )
        self.logger.info(
            'Enrolled into %d free courses.',
            len(courses['enrolled'])
        )
        self.gotify.create_message(
            title='Udemy Enrollment Summary',
            message=(
                f"Enrolled: {len(courses['enrolled'])}\n"
                f"Owned: {len(courses['owned'])}\n"
                f"Paid: {len(courses['paid'])}\n"
            )
        )

    def get_course_slug(self, udemy_url: str) -> str | None:
        """Extract and return course slug from Udemy URL."""
        url_parts = udemy_url.split('/')
        if len(url_parts) <= 4:
            self.logger.warning(
                'Malformed Udemy URL (too few segments): %s. Skipping...', udemy_url)
            return None
        course_slug: str = url_parts[4]
        return course_slug

    def run(self, email: str) -> None:
        """Orchestrate automatic enrollment into Udemy courses."""
        self.logger.info('Udemy bot starting...')
        courses: dict[str, list[str]] = {
            'owned': [],
            'paid': [],
            'enrolled': []
        }
        if not self.login(email):
            self.gotify.create_message(
                title='Udemy Login Failed',
                message='Failed to log into Udemy account.'
            )
            self.logger.error('Failed to log into Udemy. Exiting...')
            return None
        for udemy_url in self.urls:
            course_slug: str | None = self.get_course_slug(udemy_url)
            if course_slug in courses['enrolled'] + courses['owned']:
                self.logger.info(
                    '%s is already owned. Skipping...', course_slug
                )
                continue
            self.logger.info('Visiting %s', udemy_url)
            self.driver.get(udemy_url)
            self.cache.append_jsonl(
                filename='udemy.jsonl', url=udemy_url)
            course_name: str = self.driver.title.removesuffix(' | Udemy')
            if self.is_owned():
                self.logger.info('%s is owned. Skipping...', course_name)
                courses['owned'].append(course_slug)
            elif self.is_paid():
                self.logger.info('%s is paid. Skipping...', course_name)
                courses['paid'].append(course_slug)
            elif self.enroll():
                self.logger.info('Enrolling into %s', course_name)
                if self.patterns['free'] in self.driver.current_url:
                    self.logger.info('Successfully enrolled into %s',
                                     course_name)
                    self.gotify.create_message(
                        title='Udemy Enrollment Successful',
                        message=f'Enrolled into {course_name}',
                    )
                    courses['enrolled'].append(course_slug)
                    continue
                if self.confirm():
                    self.logger.info('Successfully enrolled into %s.',
                                     course_name)
                    self.gotify.create_message(
                        title='Udemy Enrollment Successful',
                        message=f'Enrolled into {course_name}',
                    )
                    courses['enrolled'].append(course_slug)
                else:
                    self.logger.info('Failed to enroll into %s', course_name)
                    self.gotify.create_message(
                        title='Udemy Enrollment Failed',
                        message=f'Failed to enroll into {course_name}'
                    )
            else:
                self.logger.info('Course is unavailable. Skipping...')
                self.gotify.create_message(
                    title='Udemy Enrollment Failed',
                    message=f'Failed to enroll into {course_name}'
                )
        self.summarize_stats(courses)
