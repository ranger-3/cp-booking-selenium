from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
    SecretStr,
    field_validator,
    model_validator,
)
from pydantic_config import SettingsModel, SettingsConfig


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
    def convert_url_to_str(cls, value: HttpUrl) -> str:
        return str(value)

    @model_validator(mode="after")
    def set_total_passengers(self) -> "Settings":
        self.total_passengers = len(self.passengers or [])
        return self


settings = Settings()
