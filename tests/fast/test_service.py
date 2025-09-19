import pytest
from selenium.common.exceptions import TimeoutException


def test_set_service_valid(service_page):
    service_page.set_service("TEST_CODE")
    service_page.wait.until.assert_called_once()


def test_set_service_not_found(service_page):
    service_page.wait.until.side_effect = TimeoutException
    with pytest.raises(TimeoutException):
        service_page.set_service("WRONG_CODE")


def test_accept_terms_valid(service_page):
    service_page.accept_terms()
    service_page.wait.until.assert_called_once()


def test_accept_terms_not_found(service_page):
    service_page.wait.until.side_effect = TimeoutException
    with pytest.raises(TimeoutException):
        service_page.accept_terms()


def test_proceed_valid(service_page):
    service_page.proceed()
    service_page.wait.until.assert_called_once()


def test_proceed_not_found(service_page):
    service_page.wait.until.side_effect = TimeoutException
    with pytest.raises(TimeoutException):
        service_page.proceed()
