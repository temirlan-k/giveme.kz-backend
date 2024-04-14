import random
from passlib.context import CryptContext


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