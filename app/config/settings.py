import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings:

    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"

    DB_URL: str = os.getenv('DB_URL')
    print(DB_URL)

    @property
    def POSTGRES_URL(self):
        return self.DB_URL



settings = Settings()
