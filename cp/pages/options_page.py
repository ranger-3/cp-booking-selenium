from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from cp.core.config import Passenger
from cp.core.constants import DISCOUNT_TYPE, DOCUMENT_TYPE
from cp.locators import options
from cp.pages.base_page import BasePage


class OptionsPage(BasePage):
    def fill_email(self, email: str) -> None:
        try:
            field = self.wait.until(EC.element_to_be_clickable(options.EMAIL_INPUT))
            field.clear()
            field.send_keys(email)
        except TimeoutException:
            raise TimeoutException("Email input not found or not clickable")

    def fill_password(self, password: str) -> None:
        try:
            field = self.wait.until(EC.element_to_be_clickable(options.PASSWORD_INPUT))
            field.clear()
            field.send_keys(password)
        except TimeoutException:
            raise TimeoutException("Password input not found or not clickable")

    def proceed(self) -> None:
        try:
            btn = self.wait.until(EC.element_to_be_clickable(options.CONTINUE_BUTTON))
            btn.click()
        except TimeoutException:
            raise TimeoutException("Continue button not found or not clickable")

    def login(self, email: str, password: str) -> None:
        self.fill_email(email)
        self.fill_password(password)
        self.proceed()

    def set_name(self, index: int, name: str) -> None:
        locator = (By.CSS_SELECTOR, f"#nome{index}")
        try:
            field = self.wait.until(EC.element_to_be_clickable(locator))
            field.clear()
            field.send_keys(name)
        except TimeoutException:
            raise TimeoutException(f"Name field not found for passenger {index}")

    def set_document_type(self, index: int, document_type: str) -> None:
        option_index = DOCUMENT_TYPE[document_type]
        locator = (By.CSS_SELECTOR, f"button[data-id='tipoIdentificacao{index}']")
        field = self.wait.until(EC.element_to_be_clickable(locator))
        field.click()

        document_type_locator = (
            By.XPATH,
            f"//div[contains(@class,'btn-group')][button[@data-id='tipoIdentificacao{index}']]//li[@data-original-index='{option_index}']/a",
        )
        option = self.wait.until(EC.element_to_be_clickable(document_type_locator))
        option.click()

    def set_document_number(self, index: int, number: str) -> None:
        locator = (By.CSS_SELECTOR, f"#identificacao{index}")
        try:
            field = self.wait.until(EC.element_to_be_clickable(locator))
            field.clear()
            field.send_keys(number)
        except TimeoutException:
            raise TimeoutException(
                f"Document number field not found for passenger {index}"
            )

    def set_discount_type(self, index: int, discount_type: str) -> None:
        try:
            button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"button[data-id='descontoview{index}']")
                )
            )
            button.click()
            option_index = DISCOUNT_TYPE[discount_type]

            option_locator = (
                By.XPATH,
                f"//div[contains(@class,'btn-group')][button[@data-id='descontoview{index}']]"
                f"//li[@data-original-index='{option_index}']/a",
            )
            option = self.wait.until(EC.element_to_be_clickable(option_locator))
            option.click()

        except TimeoutException:
            raise TimeoutException(
                f"Discount option {discount_type!r} not found for passenger {index}"
            )

    def fill_passengers(self, passengers: list[Passenger]) -> None:
        for index, passenger in enumerate(passengers):
            self.set_name(index, passenger.name)
            self.set_document_type(index, passenger.document_type)
            self.set_document_number(
                index, passenger.document_number.get_secret_value()
            )
            self.set_discount_type(index, passenger.discount_type)

        self.proceed()
        button_options = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "input#buttonNext[value='Continue >>']",
                )
            )
        )
        button_options.click()
