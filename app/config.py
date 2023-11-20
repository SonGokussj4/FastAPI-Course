from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ### DATABASE ###
    database_hostname: str
    database_port: str
    database_passport: str
    database_name: str
    database_username: str
    ### JWT ###
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
