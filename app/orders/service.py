from datetime import datetime, timedelta
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
    async def create_order(create_order_dto: OrderCreate, db: Session, current_user: dict):
        if not current_user.get('is_needer'):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only needer can order items')

        last_order = db.query(Order).filter(Order.user_id == current_user.get('id')).order_by(Order.created_at_time.desc()).first()

        if last_order:
            time_since_last_order = datetime.now() - last_order.created_at_time
            if time_since_last_order < timedelta(days=2):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You can only create one order every 48 hours')

        new_order = Order(
            contact_name=create_order_dto.contact_name,
            phone_number=create_order_dto.phone_number,
            city=create_order_dto.city,
            address=create_order_dto.address,
            user_id=current_user.get('id'),
            item_id=create_order_dto.item_id
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return {'success': True, 'msg': 'Order created successfully!', 'data': new_order}



        

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
