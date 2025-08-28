from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cohezy"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGREST_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()