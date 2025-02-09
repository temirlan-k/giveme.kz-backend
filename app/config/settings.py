import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings:

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    HASHING_ALGORITHM: str = os.getenv("HASHING_ALGORITHM")

    DB_URL: str = 'postgresql://postgres:postgres@db:5432/postgres'
    print(DB_URL)
    print(SECRET_KEY,HASHING_ALGORITHM)

    @property
    def POSTGRES_URL(self):
        print(self.SECRET_KEY,self.HASHING_ALGORITHM)

        return "postgresql://postgres:postgres@db:5432/postgres"



settings = Settings()
