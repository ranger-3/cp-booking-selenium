from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_config import SettingsConfig, SettingsModel


class Passenger(BaseModel):
    name: str
    document_type: str
    document_number: SecretStr
    discount_type: str
    carriage: int
    seat: int


class Settings(SettingsModel):
    search_page_url: HttpUrl

    headless: bool = True
    window_size: str = "1280,900"

    email: EmailStr
    password: SecretStr

    date: str
    from_station: str
    to_station: str
    service_code: str
    travel_class: str
    total_passengers: int = 0

    passengers: list[Passenger]

    model_config = SettingsConfig(env_file=".env", config_file="trip.json")

    @field_validator("search_page_url", mode="after")
    @classmethod
    def convert_url_to_str(cls, value: HttpUrl) -> str:
        return str(value)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("date must be in format DD-MM-YYYY (e.g. 19-09-2025)")
        return value

    @model_validator(mode="after")
    def set_total_passengers(self):
        self.total_passengers = len(self.passengers or [])
        return self

    @model_validator(mode="after")
    def check_stations_not_equal(self):
        if self.from_station == self.to_station:
            raise ValueError("from_station and to_station must not be the same")
        return self


settings = Settings()
