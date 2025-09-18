from pydantic import EmailStr, HttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("search_page_url", mode="after")
    def convert_url_to_str(cls, value: HttpUrl) -> str:
        return str(value)


settings = Settings()
