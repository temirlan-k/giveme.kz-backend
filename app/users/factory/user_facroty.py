

from fastapi import HTTPException,status
from app.users.models import User
from app.users.utils import Hash


class UserFactory:

    @staticmethod
    def _check_user_password(user:User, password:str):
        if not Hash.verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
       