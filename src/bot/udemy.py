"""Automatically enroll into free Udemy courses."""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Udemy:
    """Autoenroll into free Udemy courses."""

    def __init__(self, *, driver: WebDriver, urls: set[str]) -> None:
        self.driver = driver
        self.urls = urls

    def enroll(self, wait) -> None:
        """Click on first 'Enroll now' button."""
        buttons = wait.until(lambda d: d.find_elements(
            By.XPATH,
            "//button[@data-purpose='buy-this-course-button' and contains(., 'Enroll')]",
        ))
        enroll_button = next(
            (b for b in buttons if b.is_displayed() and b.is_enabled()), None)
        print(f"Clicking visible enroll button: {enroll_button.text}")
        enroll_button.click()
        print("Clicked first enroll button!")

    def confirm(self, wait) -> None:
        """Click on final 'Enroll now' button."""
        enroll_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="udemy"]/div[1]/div[2]/div/div/div/aside/div/div/div[2]/div[2]/button[1]'
        )))
        print("Clicked final enroll button!")
        enroll_button.click()

    def run(self) -> None:
        """Orchestrate automatic enrollment into Udemy courses."""
        for udemy_url in self.urls:
            try:
                self.driver.get(udemy_url)
                print("Udemy page title:", self.driver.title)
                wait = WebDriverWait(self.driver, 10)
                self.enroll(wait)
                self.confirm(wait)
            except (AttributeError, TimeoutException):
                print('Enroll button not found! Skipping...')
                continue
