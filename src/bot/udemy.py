"""Automatically enroll into free Udemy courses."""
import random
import time
from pathlib import Path

import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from client.gmail import GmailClient
from config.bot import BotConfig
from utils.cache import Cache
from utils.logger import setup_logging


class Udemy:
    """Autoenroll into free Udemy courses."""

    def __init__(self, *, driver: uc.Chrome, urls: list[str],
                 config: BotConfig) -> None:
        self.cache = Cache()
        self.driver = driver
        self.logger = setup_logging()
        self.config = config
        self.urls = urls
        self.patterns = {'confirm': 'cart/success', 'free': 'cart/subscribe'}
        self.wait = WebDriverWait(self.driver, timeout=self.config.timeout)

    def enter_email(self, email: str):
        """Enter email into login form."""
        for retry in range(self.config.retries):
            try:
                container = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".ud-compact-form-control-container")))
                container.click()
                email_input = self.wait.until(
                    EC.visibility_of_element_located((By.NAME, 'email')))
                email_input.clear()
                email_input.send_keys(email)
                self.logger.info('Entered email successfully.')
                return
            except WebDriverException:
                self.logger.error(
                    'Error entering email (attempt %d/%d)',
                    retry+1,
                    self.config.retries
                )
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))

    def click_login_btn(self) -> None:
        """Click on the login button on Udemy homepage."""
        for retry in range(self.config.retries):
            try:
                login_button: uc.WebElement = self.wait.until(EC.element_to_be_clickable((
                    By.LINK_TEXT,
                    'Log in'
                )))
                login_button.click()
            except WebDriverException:
                self.logger.error(
                    'Error clicking login button (attempt %d/%d)',
                    retry+1,
                    self.config.retries
                )
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout
                ))

    def click_purple_button(self, text: str) -> None:
        """Click on the Continue button after entering email."""
        for retry in range(self.config.retries):
            try:
                continue_btn = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         f"//button[.//span[normalize-space()='{text}']]")
                    )
                )
                continue_btn.click()
            except WebDriverException as e:
                self.logger.error(
                    f'Error clicking {text} button (attempt %d/%d): %s',
                    retry+1,
                    self.config.retries,
                    e
                )
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout
                ))

    def enter_code(self, code: str) -> bool:
        """Enter verification code into login form."""
        for retry in range(self.config.retries):
            try:
                container = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".ud-compact-form-control-container")))
                container.click()
                code_input = self.wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'input.ud-text-input.ud-text-input-medium.ud-text-sm.ud-compact-form-control'))
                )
                code_input.clear()
                code_input.send_keys(code)
                self.logger.info(
                    'Entered 6-digit verification code successfully.')
                return True
            except WebDriverException as e:
                self.logger.error(
                    'Error entering 6-digit code (attempt %d/%d): %s',
                    retry+1,
                    self.config.retries,
                    e
                )
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))
        return False

    def login(self, email: str) -> None:
        """Log into Udemy account."""
        self.driver.get('https://www.udemy.com/')
        self.wait: WebDriverWait = WebDriverWait(
            self.driver, timeout=self.config.timeout)

        self.click_login_btn()
        self.enter_email(email)
        self.click_purple_button(text='Continue')
        gmail_client: GmailClient = GmailClient(
            client_secret=Path(self.config.gmail_client_secret)
        )
        time.sleep(self.config.timeout)
        code: str = gmail_client.get_verification_code()
        if not code:
            self.logger.error(
                'Failed to retrieve verification code from email.')
            raise SystemExit('Exiting...')
        self.logger.info('Retrieved verification code: %s', code)
        self.enter_code(code)
        self.logger.info('Entered verification code successfully.')
        time.sleep(self.config.timeout)
        self.click_purple_button(text='Log in')
        self.logger.info('Logged into Udemy successfully.')

    def get_enroll_button(self, text: str) -> uc.WebElement | None:
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

    def get_confirm_button(self) -> uc.WebElement | None:
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
            _button: uc.WebElement | None = self.get_enroll_button(
                text='Go to course')
            return True
        except WebDriverException:
            return False

    def is_paid(self) -> bool:
        """Return a flag whether course is paid."""
        try:
            _button: uc.WebElement = self.get_enroll_button(text='Buy now')
            return True
        except WebDriverException:
            return False

    def is_not_accepting_enrollments(self) -> bool:
        """Return a flag indicating whether the course is not accepting enrollments."""
        self.logger.info('Checking if course is not accepting enrollments...')
        message_xpath = (
            "//h2[contains(normalize-space(), "
            "'Sorry, this course is no longer accepting enrollments.')]"
        )
        try:
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, message_xpath)))
            return True
        except WebDriverException:
            return False

    def click_radio_button(self) -> None:
        """Click on the radio button for free course enrollment."""
        self.logger.info('Clicking radio button for free course enrollment...')
        wait: WebDriverWait = WebDriverWait(
            self.driver, timeout=self.config.timeout)
        button_xpath: str = (
            "//span[contains(text(), 'Buy individual course')]"
        )
        for attempt in range(self.config.retries):
            try:
                radio_button: uc.WebElement = wait.until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                radio_button.click()
                self.logger.info('Clicked radio button successfully.')
                return
            except WebDriverException:
                self.logger.warning('Attempt %d/%d failed.',
                                    attempt+1,
                                    self.config.retries)
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))

    def click_enroll_now(self) -> None:
        """Scan for first 'Enroll now' button and click on it."""
        self.logger.info('Clicking first Enroll now button...')
        for attempt in range(self.config.retries):
            try:
                enroll_button: uc.WebElement = self.get_enroll_button(
                    text='Enroll now')
                enroll_button.click()
                self.logger.info('Attempt %d/%d succeeded!',
                                 attempt+1,
                                 self.config.retries)
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))
                return
            except WebDriverException:
                self.logger.warning('Attempt %d/%d failed.',
                                    attempt+1,
                                    self.config.retries)
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))
                continue

    def confirm(self) -> None:
        """Scan for final 'Enroll now' button and click on it."""
        for attempt in range(self.config.retries):
            try:
                confirm_button: uc.WebElement = self.get_confirm_button()
                confirm_button.click()
                self.logger.info('Attempt %d/%d succeeded!',
                                 attempt+1,
                                 self.config.retries)
                return
            except WebDriverException:
                self.logger.warning('Attempt %d/%d failed.',
                                    attempt+1,
                                    self.config.retries)
                time.sleep(random.uniform(
                    self.config.timeout/2, self.config.timeout))

    def enroll(self, course_name: str) -> None:
        """Orchestrate enrollment flow for free Udemy course."""
        self.logger.info('Enrolling into %s', course_name)
        self.click_radio_button()
        self.click_enroll_now()
        if self.patterns['free'] in self.driver.current_url:
            self.logger.info('Successfully enrolled into %s',
                             course_name)
            return
        self.confirm()
        if self.patterns['confirm'] in self.driver.current_url:
            self.logger.info('Successfully enrolled into %s.', course_name)

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
        self.login(email)
        for udemy_url in self.urls:
            self.logger.info('Visiting %s', udemy_url)
            self.driver.get(udemy_url)
            self.cache.append_jsonl(
                filename='udemy.jsonl',
                url=udemy_url
            )
            if self.is_not_accepting_enrollments():
                self.logger.info(
                    'Course is not accepting enrollments. Skipping...'
                )
                continue
            course_name: str = self.driver.title.removesuffix(' | Udemy')
            if self.is_owned():
                self.logger.info('%s is owned. Skipping...', course_name)
            elif self.is_paid():
                self.logger.info('%s is paid. Skipping...', course_name)
            else:
                self.enroll(course_name)
