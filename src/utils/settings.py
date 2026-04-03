from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env", extra="ignore")

    GOOGLE_CLOUD_CLIENT_ID: str
    GOOGLE_CLOUD_CLIENT_ID_2: str
    DB_CONNECTION: str
    ALGORITHM: str
    SECRET_KEY: str


settings = Settings() #type:ignore