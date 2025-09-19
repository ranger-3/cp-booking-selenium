import pytest
from selenium.common.exceptions import TimeoutException


def test_same_route_raises(search_page):
    with pytest.raises(ValueError):
        search_page.set_route("Barcelos", "Barcelos")


@pytest.mark.parametrize(
    "passengers",
    [0, 10, -1],
    ids=["zero", "too_many", "negative"],
)
def test_passengers_out_of_range(search_page, passengers):
    with pytest.raises(ValueError):
        search_page.set_passengers(passengers)


@pytest.mark.parametrize(
    "bad_class",
    [
        "luxury",
        "vip",
        "economy+",
        " ",
        "",
        "nonsense",
        "foobar",
        "123",
    ],
)
def test_invalid_travel_class(search_page, bad_class):
    with pytest.raises(ValueError):
        search_page.set_travel_class(bad_class)


@pytest.mark.parametrize(
    "bad_date",
    [
        "31-02-2025",
        "32-01-2025",
        "29-02-2023",
        "00-12-2025",
    ],
)
def test_set_date_invalid_calendar(search_page, bad_date):
    with pytest.raises(ValueError):
        search_page.set_date(bad_date)


@pytest.mark.parametrize(
    "bad_date",
    [
        "2025/09/24",
        "24.09.2025",
        "09-24-2025",
        "2025-09-24",
        "24-9-25",
        "abcdef",
        "",
        "   ",
    ],
)
def test_set_date_wrong_format(search_page, bad_date):
    with pytest.raises(ValueError):
        search_page.set_date(bad_date)


@pytest.mark.parametrize("passengers", range(1, 10))
def test_set_passengers_valid(search_page, passengers):
    search_page.set_passengers(passengers)


@pytest.mark.parametrize("travel_class", ["comfort", "Comfort", "tourist", "TOURIST"])
def test_set_travel_class_valid(search_page, travel_class):
    search_page.set_travel_class(travel_class)


def test_set_date_valid(faker, search_page):
    search_page.set_date(faker.future_date().strftime("%d-%m-%Y"))


def test_set_route_valid(search_page):
    search_page.set_route("Barcelos", "Ademia")


def test_set_route_invalid_from_station(search_page):
    search_page.wait.until.return_value.get_attribute.return_value = "ng-invalid"
    with pytest.raises(ValueError):
        search_page.set_route("Fake Station", "Ademia")


def test_set_route_invalid_to_station(search_page):
    search_page.wait.until.return_value.get_attribute.side_effect = ["", "ng-invalid"]
    with pytest.raises(ValueError):
        search_page.set_route("Barcelos", "Fake Station")


def test_submit_valid(search_page):
    search_page.submit()


def test_submit_invalid(search_page):
    search_page.wait.until.side_effect = TimeoutException
    with pytest.raises(ValueError):
        search_page.submit()
