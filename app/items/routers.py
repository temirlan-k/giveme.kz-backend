from typing import Dict, List
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    File,
    Form,
    Query,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.auth.auth_bearer import JWTBearer
from app.config.db import get_db
from app.items.models import Item
from app.items.schemas import ItemCreate
from app.items.service import ItemService
from app.users.service import UserService

router = APIRouter(tags=["items"])


@router.post("/item/create", dependencies=[Depends(JWTBearer())])
async def create_item(
        item_file: UploadFile = File(...),
        category_id: int = Form(...),
        contact_phone_number:str = Form(...),
        contact_address:str = Form(...),
        db: Session = Depends(get_db),
        current_user: dict = Depends(UserService.get_current_user),
        ):
    return await ItemService.create_item(item_file, category_id,contact_phone_number,contact_address, db, current_user)


@router.get("/items/")
async def get_items(cat: List[str] = Query(None), db: Session = Depends(get_db)):
    return await ItemService.get_items_by_category(cat, db)


@router.get('/items/my_items',dependencies=[Depends(JWTBearer())])
async def get_user_items(db: Session = Depends(get_db),current_user : dict = Depends(UserService.get_current_user)):
    return await ItemService.get_my_items(db,current_user)