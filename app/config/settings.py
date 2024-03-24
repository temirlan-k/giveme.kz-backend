import os
from pydantic_settings import BaseSettings
from decouple import config
class Settings(BaseSettings):


    #Security
    SECRET_KEY: str = config("SECRET_KEY")
    HASHING_ALGORITHM: str = config("HASHING_ALGORITHM")

    # DB Settings
    DB_URL:str = config('DB_URL',cast=str)

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def POSTGRES_URL(self):
        # url = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB}"
        return self.DB_URL
    
settings = Settings()