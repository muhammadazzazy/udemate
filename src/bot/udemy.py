"""Automatically enroll into free Udemy courses."""
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import setup_logging


class Udemy:
    """Autoenroll into free Udemy courses."""

    def __init__(self, driver: WebDriver, urls: set[str]) -> None:
        self.driver = driver
        self.urls = urls
        self.logger = setup_logging()
        self.pattern = 'cart/success'

    def confirm(self) -> bool:
        """Scan for final 'Enroll now' button and click on it."""
        try:
            flag: bool = False
            wait = WebDriverWait(self.driver, 30)
            confirm_button = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="udemy"]/div[1]/div[2]/div/div/div/aside/div/div/div[2]/div[2]/button[1]'
            )))
            confirm_button.click()
            time.sleep(3)
            if self.pattern in self.driver.current_url:
                flag = True
            return flag
        except WebDriverException as e:
            self.logger.error('Webdriver error: %s', e)
            return flag

    def is_owned(self) -> bool:
        """Return a flag indicating whether a course is owned."""
        try:
            wait = WebDriverWait(self.driver, 5)
            _buttons = wait.until(lambda d: d.find_elements(
                By.XPATH,
                "//button[@data-purpose='buy-this-course-button' and contains(., 'Go to course')]",
            ))
            return True
        except WebDriverException:
            return False

    def is_paid(self) -> bool:
        """Return a flag whether course is paid."""
        try:
            wait = WebDriverWait(self.driver, 5)
            _buttons = wait.until(lambda d: d.find_elements(
                By.XPATH,
                "//button[@data-purpose='buy-this-course-button' and contains(., 'Buy now')]",
            ))
            return True
        except WebDriverException:
            return False

    def enroll(self) -> bool:
        """Scan for first 'Enroll now' button and click on it."""
        try:
            wait = WebDriverWait(self.driver, 5)
            buttons = wait.until(lambda d: d.find_elements(
                By.XPATH,
                "//button[@data-purpose='buy-this-course-button' and contains(., 'Enroll now')]",
            ))
            enroll_button = next(
                (b for b in buttons if b.is_displayed() and b.is_enabled()), None)
            enroll_button.click()
            return True
        except WebDriverException:
            return False

    def run(self) -> None:
        """Orchestrate automatic enrollment into Udemy courses."""
        self.logger.info('Udemy bot starting...')
        for udemy_url in self.urls:
            self.logger.info('Visiting %s', udemy_url)
            self.driver.get(udemy_url)
            course_name: str = self.driver.title.removesuffix(' | Udemy')
            if self.is_owned():
                self.logger.info('%s is owned. Skipping...', course_name)
            elif self.is_paid():
                self.logger.info('%s is paid. Skipping...', course_name)
            elif self.enroll():
                self.logger.info('Enrolling into %s', course_name)
                if self.confirm():
                    self.logger.info('Successfully enrolled into %s.',
                                     course_name)
                else:
                    self.logger.info('Failed to enroll into %s', course_name)
            else:
                # "Unavailable" means private or does not exist.
                self.logger.info('Course is unavailable. Skipping...')
