import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    HASHING_ALGORITHM: str = os.getenv("HASHING_ALGORITHM")

    # DB Settings
    DB_URL: str = os.getenv("DB_URL")

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def POSTGRES_URL(self):
        return self.DB_URL



settings = Settings()
