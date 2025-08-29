from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Cohezy"
    admin_email: str = "letuankiet0012@gmail.com"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGREST_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int = 0

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()