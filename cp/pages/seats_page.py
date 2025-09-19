from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from cp.core.config import SeatSpec
from cp.locators import seats
from cp.pages.base_page import BasePage


class SeatsPage(BasePage):
    def set_seats(self, seats_spec: list[SeatSpec]) -> None:
        seat_ids: list[str] = []

        for spec in seats_spec:
            img = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//img[@title='{spec.seat}' or @alt='{spec.seat}']"
                        f"[contains(@data-id, '_{spec.carriage}_')]",
                    )
                )
            )
            seat_id = img.get_attribute("data-id")
            if not seat_id:
                raise RuntimeError(
                    f"No data-id for carriage {spec.carriage}, seat {spec.seat}"
                )

            status = seat_id.split(":")[-1]
            if status not in {"0", "2"}:
                raise RuntimeError(
                    f"Seat {spec.seat} in carriage {spec.carriage} not free (id={seat_id})"
                )

            seat_ids.append(seat_id)

        seat_ids_str = ";".join(seat_ids)

        self.driver.execute_script(
            """
            const value = arguments[0];
            const tripSeats = document.getElementById('tripSeats');
            tripSeats.value = value;
            if (window.seats) window.seats = value.split(';');
            if (window.oldSeats) window.oldSeats = value.split(';');
            """,
            seat_ids_str,
        )

    def proceed(self) -> None:
        try:
            continue_button = self.wait.until(
                EC.element_to_be_clickable(seats.CONTINUE_BUTTON)
            )
            continue_button.click()
        except TimeoutException:
            raise TimeoutException("Could not find or click Continue button")

        try:
            confirm_button = self.wait.until(
                EC.element_to_be_clickable(seats.KEEP_SEATS_BUTTON)
            )
            confirm_button.click()
        except TimeoutException:
            raise TimeoutException("Could not find or click Keep Seats button")
