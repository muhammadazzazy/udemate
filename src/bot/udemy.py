"""Automatically enroll into free Udemy courses."""
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bot.base import Bot


class Udemy(Bot):
    """Autoenroll into free Udemy courses."""

    def enroll(self, wait) -> None:
        """Click on first 'Enroll now' button."""
        buttons = wait.until(lambda d: d.find_elements(
            By.XPATH,
            "//button[@data-purpose='buy-this-course-button' and contains(., 'Enroll')]",
        ))
        enroll_button = next(
            (b for b in buttons if b.is_displayed() and b.is_enabled()), None)
        enroll_button.click()
        enroll_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="udemy"]/div[1]/div[2]/div/div/div/aside/div/div/div[2]/div[2]/button[1]'
        )))
        enroll_button.click()

    def run(self) -> None:
        """Orchestrate automatic enrollment into Udemy courses."""
        for udemy_url in self.urls:
            try:
                self.driver.get(udemy_url)
                course_name: str = self.driver.title.removesuffix(' | Udemy')
                self.logger.info(course_name)
                wait = WebDriverWait(self.driver, 30)
                self.enroll(wait)
                self.logger.info('Successfully enrolled into %s', course_name)
                time.sleep(2)
            except (AttributeError, WebDriverException):
                self.logger.exception('Enroll button not found! Skipping...')
                continue
