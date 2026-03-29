from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env", extra="ignore")

    GOOGLE_CLOUD_CLIENT_ID: str
    DB_CONNECTION: str


settings = Settings() #type:ignore