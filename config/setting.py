import os
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    # 24 horas
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Setting()
