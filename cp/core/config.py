from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Passenger(BaseModel):
    name: str
    document_type: str
    document_number: str
    discount_type: str


class Settings(BaseSettings):
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
    passengers: int

    passengers_data: list[Passenger]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("search_page_url", mode="after")
    def convert_url_to_str(cls, value: HttpUrl) -> str:
        return str(value)


settings = Settings()
