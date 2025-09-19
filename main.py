import sys

from cp.core.config import settings
from cp.core.driver import create_driver
from cp.pages.options_page import OptionsPage
from cp.pages.search_page import SearchPage
from cp.pages.seats_page import SeatsPage
from cp.pages.service_page import ServicePage


def main() -> int:
    driver = create_driver(settings.headless, settings.window_size)

    try:
        search_page = SearchPage(driver)
        search_page.open()
        search_page.accept_cookies()

        search_page.set_passengers(settings.passengers)
        search_page.set_travel_class(settings.travel_class)
        search_page.set_date(settings.date)
        search_page.set_route(settings.from_station, settings.to_station)
        search_page.submit()

        service_page = ServicePage(driver)
        service_page.set_service(settings.service_code)
        service_page.accept_terms()
        service_page.proceed()

        options_page = OptionsPage(driver)
        options_page.login(settings.email, settings.password.get_secret_value())
        options_page.fill_passengers(settings.passengers_data)

        seats_page = SeatsPage(driver)
        seats_page.set_seats(settings.seats_spec)
        seats_page.proceed()

        return 0
    finally:
        driver.quit()


if __name__ == "__main__":
    sys.exit(main())
