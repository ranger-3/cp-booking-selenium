from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from cp.locators import service
from cp.pages.base_page import BasePage


class ServicePage(BasePage):
    def set_service(self, service_code: str) -> None:
        locator = (
            By.XPATH,
            f"//span[@class='nobr' and normalize-space(text())='{service_code}']",
        )

        try:
            button = self.wait.until(EC.element_to_be_clickable(locator))
            button.click()
        except TimeoutException:
            raise TimeoutException(f"Could not find train {service_code}")

    def accept_terms(self) -> None:
        checkbox = self.wait.until(EC.element_to_be_clickable(service.TERMS_CHECKBOX))
        checkbox.click()
