from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from cp.locators import options
from cp.pages.base_page import BasePage


class OptionsPage(BasePage):
    def _fill_email(self, email: str) -> None:
        try:
            field = self.wait.until(EC.element_to_be_clickable(options.EMAIL_INPUT))
            field.clear()
            field.send_keys(email)
        except TimeoutException:
            raise TimeoutException("Email input not found or not clickable")

    def _fill_password(self, password: str) -> None:
        try:
            field = self.wait.until(EC.element_to_be_clickable(options.PASSWORD_INPUT))
            field.clear()
            field.send_keys(password)
        except TimeoutException:
            raise TimeoutException("Password input not found or not clickable")

    def _proceed(self) -> None:
        try:
            btn = self.wait.until(EC.element_to_be_clickable(options.CONTINUE_BUTTON))
            btn.click()
        except TimeoutException:
            raise TimeoutException("Continue button not found or not clickable")

    def login(self, email: str, password: str) -> None:
        self._fill_email(email)
        self._fill_password(password)
        self._proceed()
