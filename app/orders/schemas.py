from pydantic import Field,BaseModel,UUID4

class OrderCreate(BaseModel):
    contact_name :str = Field(...,max_length=50,min_length=2)
    phone_number :str = Field(...,max_length=20)
    city :str = Field(...,max_length=100,min_length=2)
    address :str = Field(...,max_length=255,min_length=2)
    item_id:UUID4


    class Config:
        from_attribute = True