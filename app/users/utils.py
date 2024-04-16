import random
from fastapi import UploadFile
from passlib.context import CryptContext

from app.config.aws import upload_needer_file
from app.items.utils import validate_file_size_type


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def hash_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)


def validate_field_to_starts_with_uppercase(field):
    if field[0].islower():
        raise ValueError("Name and Surname must start with an uppercase letter")
    return field


def generate_code():
    return random.randint(100000000, 999999999)


async def upload_and_validate_file(file: UploadFile):
    await validate_file_size_type(file)
    return await upload_needer_file(file)
