from pydantic import BaseModel, validator, Field
from typing import List, Union


class ItemCreate(BaseModel):
    category_id: int = Field(..., gt=1)

    @validator("category_id")
    def check_category_id(cls, v):
        v = int(v)
        if v < 1 or v > 3:
            raise ValueError("category_id must be between 1 and 3")
        return v
