from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Digital Freight Desk API"
    db_url: str = "sqlite:///./freightdesk.db"
    dev_api_key: str = "dev-admin-key"


settings = Settings()
