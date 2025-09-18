from selenium.webdriver.common.by import By

ACCEPT_COOKIES = (By.LINK_TEXT, "Accept all cookies")

FROM_INPUT = (By.CSS_SELECTOR, "#searchTimetableForm input[name='textBoxPartida']")
TO_INPUT = (By.CSS_SELECTOR, "#searchTimetableForm input[name='textBoxChegada']")

DEPARTURE_DATE = (By.CSS_SELECTOR, "#searchTimetableForm #datepicker-first")

CLASS_COMFORT_LABEL = (By.CSS_SELECTOR, "#searchTimetableForm #option1Label")
CLASS_TOURIST_LABEL = (By.CSS_SELECTOR, "#searchTimetableForm #option2Label")

PASSENGERS_DROPDOWN = (
    By.CSS_SELECTOR,
    "#searchTimetableForm button[data-id='nr_passageiros']",
)

SUBMIT_BUTTON = (By.CSS_SELECTOR, "#searchTimetableForm input.btn-primary")
