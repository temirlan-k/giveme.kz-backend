from sqlalchemy.orm import Session
from fastapi import (
    Body,
    Depends,
    Form,
    HTTPException,
    status,
    UploadFile,
    File,
)
from app.config.db import get_db
from app.items.models import Category, Item
from app.orders.models import Order
from app.orders.schemas import OrderCreate
from app.users.service import UserService


class OrderService:


    async def create_order(create_order_dto: OrderCreate = Body(...),db: Session = Depends(get_db),current_user: dict =Depends(UserService.get_current_user)):
        try:
            if not current_user.get('is_needer'):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Only needer can order items')
            
            db_order = Order(
                contact_name=create_order_dto.contact_name,
                phone_number=create_order_dto.phone_number,
                city=create_order_dto.city,
                address=create_order_dto.address,
                user_id = current_user.get('id'),
                    item_id = create_order_dto.item_id
            )
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            return {'success':True,'msg':'Order created successfully!','data':db_order}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def get_my_orders(db: Session = Depends(get_db), current_user: dict = Depends(UserService.get_current_user)):
        user_orders = db.query(Order, Item, Category).\
            join(Item, Order.item_id == Item.id).\
            join(Category, Item.category_id == Category.id).\
            filter(Order.user_id == current_user.get('id')).\
            all()

        orders = []
        for order, item, category in user_orders:
            order_details = {
                "order_id": order.id,
                "contact_name": order.contact_name,
                "address": order.address,
                "city": order.city,
                "phone_number": order.phone_number,
                "status":order.status,
                "item": {
                    "id": item.id,
                    "image": item.image,
                    "category_name": category.name  
                }
            }
            orders.append(order_details)

        return orders
