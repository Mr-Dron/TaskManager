from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    APP_DB_USER: str
    APP_DB_PASSWORD: str
    APP_DB_NAME: str

    #Minio
    MINIO_USER: str
    MINIO_PASSWORD: str

    #Redis
    REDIS_HOST: str
    REDIS_PORT: int
    
    DATABASE_URL: str

    GRAFANA_PASS: str

    #Token
    VERIFICATION_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SECRET_KEY: str

    #email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM_NAME: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_STARTTLS: bool
    MAIL_SSL: bool 

    APP_DOMAIN: str
    VEREFICATION_TOKEN_EXPIRE_MINUTES: int



    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()