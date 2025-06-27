"""Automatically enroll into free Udemy courses."""
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

    def confirm(self, wait) -> None:
        """Scan for final 'Enroll now' button and click on it."""
        confirm_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="udemy"]/div[1]/div[2]/div/div/div/aside/div/div/div[2]/div[2]/button[1]'
        )))
        confirm_button.click()

    def enroll(self, url: str) -> str:
        """
        Return name of course.
        Scan for first 'Enroll now' button and click on it.
        """
        self.driver.get(url)
        course_name: str = self.driver.title.removesuffix(' | Udemy')
        wait = WebDriverWait(self.driver, 30)
        buttons = wait.until(lambda d: d.find_elements(
            By.XPATH,
            "//button[@data-purpose='buy-this-course-button' and contains(., 'Enroll')]",
        ))
        enroll_button = next(
            (b for b in buttons if b.is_displayed() and b.is_enabled()), None)
        enroll_button.click()
        return course_name

    def run(self) -> None:
        """Orchestrate automatic enrollment into Udemy courses."""
        for udemy_url in self.urls:
            try:
                self.logger('Visiting %s', udemy_url)
                course_name: str = self.scrape(udemy_url)
                self.logger.info('Successfully enrolled into %s', course_name)
            except (AttributeError, WebDriverException):
                self.logger.info('Enroll button not found! Skipping...')
                continue
