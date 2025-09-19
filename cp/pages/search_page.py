from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from cp.core.config import settings
from cp.locators import search
from cp.pages.base_page import BasePage


class SearchPage(BasePage):
    URL = settings.search_page_url

    def open(self) -> None:
        self.driver.get(self.URL)

    def accept_cookies(self) -> None:
        try:
            button = self.wait.until(EC.element_to_be_clickable(search.ACCEPT_COOKIES))
            button.click()
        except TimeoutException:
            pass

    def set_travel_class(self, travel_class: str) -> None:
        travel_class = travel_class.lower()

        if travel_class == "comfort":
            locator = search.CLASS_COMFORT_LABEL
        elif travel_class == "tourist":
            locator = search.CLASS_TOURIST_LABEL
        else:
            raise ValueError(
                f"Unknown class: {travel_class!r}. Use 'comfort' or 'tourist'"
            )

        try:
            button = self.wait.until(EC.element_to_be_clickable(locator))
            button.click()
        except TimeoutException:
            raise TimeoutException(
                f"Travel class button not found or not clickable: {travel_class!r}"
            )

    def set_route(self, from_station: str, to_station: str) -> None:
        from_input = self.wait.until(EC.element_to_be_clickable(search.FROM_INPUT))
        from_input.clear()
        from_input.send_keys(from_station)

        from_input = self.wait.until(EC.element_to_be_clickable(search.FROM_INPUT))
        classes = from_input.get_attribute("class") or ""
        if "ng-invalid" in classes:
            raise ValueError(
                f"Departure station {from_station!r} not recognized by CP site"
            )

        to_input = self.wait.until(EC.element_to_be_clickable(search.TO_INPUT))
        to_input.clear()
        to_input.send_keys(to_station)

        to_input = self.wait.until(EC.element_to_be_clickable(search.TO_INPUT))
        classes = to_input.get_attribute("class") or ""
        if "ng-invalid" in classes:
            raise ValueError(
                f"Arrival station {to_station!r} not recognized by CP site"
            )

    def set_date(self, date: str) -> None:
        parsed_date = datetime.strptime(date, "%d-%m-%Y")
        formatted_date = parsed_date.strftime("%d %B, %Y")

        departure_date = self.wait.until(
            EC.element_to_be_clickable(search.DEPARTURE_DATE)
        )
        departure_date.clear()
        departure_date.send_keys(formatted_date)

        departure_date = self.wait.until(
            EC.element_to_be_clickable(search.DEPARTURE_DATE)
        )
        classes = departure_date.get_attribute("class") or ""
        if "ng-invalid" in classes:
            raise ValueError(
                f"Departure date {formatted_date!r} not accepted by CP site"
            )

    def set_passengers(self, total: int) -> None:
        if not (1 <= total <= 9):
            raise ValueError(f"Passengers must be in 1..9, got {total!r}")

        try:
            passengers_button = self.wait.until(
                EC.element_to_be_clickable(search.PASSENGERS_DROPDOWN)
            )
            passengers_button.click()
        except TimeoutException:
            raise TimeoutException("Passengers button not found or not clickable")

        try:
            passenger_option = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        f"#searchTimetableForm li[data-original-index='{total - 1}']",
                    )
                )
            )
            passenger_option.click()
        except TimeoutException:
            raise TimeoutException(
                f"Passenger option {total} not found or not clickable"
            )

    def submit(self) -> None:
        try:
            button = self.wait.until(EC.element_to_be_clickable(search.SUBMIT_BUTTON))
        except TimeoutException:
            raise ValueError("Form is invalid, submit button never became clickable")

        button.click()
