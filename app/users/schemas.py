from pydantic import BaseModel, Field, EmailStr, validator


class UserCreate(BaseModel):
    name: str = Field(..., alias="Name", min_length=2, max_length=50)
    surname: str = Field(..., alias="Surname", min_length=2, max_length=50)
    email: EmailStr = Field(..., alias="Email", min_length=4, max_length=320)
    password: str = Field(..., alias="Password", max_length=64, min_length=8)

    @validator("name")
    def validate_name_custom(cls, v):
        if v[0].islower():
            raise ValueError("Name must start with an uppercase letter")
        return v

    @validator("surname")
    def validate_surname_custom(cls, v):
        if v[0].islower():
            raise ValueError("Surname must start with an uppercase letter")
        return v

    @validator("password")
    def validate_password(cls, password):
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if all(char.isalnum() for char in password):
            raise ValueError("Password must contain at least one special character")
        return password


class UserLogin(BaseModel):
    email: EmailStr = Field(..., alias="Email", min_length=4, max_length=320)
    password: str = Field(..., alias="Password", max_length=64, min_length=8)


class ForgetPasswordRequest(BaseModel):
    email: EmailStr = Field(..., alias="Email", min_length=4, max_length=320)


class ResetForgetPassword(BaseModel):
    new_password: str = Field(..., alias="Password", max_length=64, min_length=8)
    confirm_password: str = Field(
        ..., alias="Confirm_password", max_length=64, min_length=8
    )

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class CurrentUserOut(BaseModel):
    name: str
    surname: str
    email: EmailStr
    is_needer: bool
    role: str
