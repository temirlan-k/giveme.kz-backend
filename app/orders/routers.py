from fastapi import APIRouter
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
from app.orders.service import OrderService
from app.orders.schemas import OrderCreate
from app.users.service import UserService

router = APIRouter(tags=['orders'])

@router.post('/order/create',dependencies=[Depends(JWTBearer())])
async def create_order(create_order_dto: OrderCreate = Body(...) ,
                       db: Session = Depends(get_db),
                       current_user: dict =Depends(UserService.get_current_user)):
    return await OrderService.create_order(create_order_dto,db,current_user)

@router.get('/orders/my_orders',dependencies=[Depends(JWTBearer())])
async def get_my_orders(db: Session = Depends(get_db), current_user: dict =Depends(UserService.get_current_user)):
    return await OrderService.get_my_orders(db,current_user)