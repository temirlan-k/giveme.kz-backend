from fastapi import UploadFile
from pydantic import BaseModel, Field, validator
import re

class ItemCreate(BaseModel):
    category_id: int
    contact_phone_number: str
    contact_address: str

    @validator("category_id")
    def check_category_id(cls, v):
        if v < 1 or v > 3:
            raise ValueError("category_id must be between 1 and 3")
        return v

    @validator("contact_phone_number")
    def check_contact_phone_number(cls, v):
        if not re.match(r'^\+?\d{1,3}[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$', v):
            raise ValueError("Invalid phone number format")
        return v

    @validator("contact_address")
    def check_contact_address(cls, v):
        if not v:
            raise ValueError("Contact address cannot be empty")
        return v
