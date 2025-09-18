from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from cp.pages.base_page import BasePage


class ServicePage(BasePage):
    def set_service(self, train_code: str):
        locator = (
            By.XPATH,
            f"//span[@class='nobr' and normalize-space(text())='{train_code}']",
        )

        try:
            button = self.wait.until(EC.element_to_be_clickable(locator))
            button.click()
        except TimeoutException:
            raise TimeoutException(f"Could not find train {train_code}")

        return self
