import json
from typing import List
from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    Form,
    HTTPException,
    status,
    UploadFile,
    File,
)
from app.config.aws import upload_item_photo
from app.config.db import get_db
from app.config.settings import settings
from app.items.models import Item, Category
from app.items.schemas import ItemCreate
from app.items.utils import validate_file_size_type
from app.users.service import UserService




class ItemService:

    async def create_item(
        file: UploadFile = File(...),
        category_id: int = Form(...),
        db: Session = Depends(get_db),
        current_user: dict = Depends(UserService.get_current_user),
    ):
      
        await validate_file_size_type(file)

        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist.")
        try:

            s3_db_key = await upload_item_photo(file)

            db_item = Item(
                image=s3_db_key, category_id=category_id, user_id=current_user.get("id")
            )

            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return {"success": True, "user": current_user.get("id"), "link": s3_db_key}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file: {str(e)}"
            )

    async def get_items_by_category(category_names: List[str] = None, db: Session = Depends(get_db)):
            
            items_with_category_name = []
            query = db.query(Item).filter(Item.is_publish==True)

            if category_names:
                  category_names_upper = [category_name.upper() for category_name in category_names]

                  categories = db.query(Category).filter(Category.name.in_(category_names_upper)).all()
                  category_id_map = {category.name.upper(): category.id for category in categories}

                  for category_name in category_names:
                        category_id = category_id_map.get(category_name.upper())
                        if category_id is None:
                              raise HTTPException(
                                    status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Category {category_name} Not Found",
                              )

                        items = query.filter(Item.category_id == category_id).all()
                        items_with_category_name.extend(
                        {**item.__dict__, "category_name": category_name.upper()} for item in items
                        )
            else:
                  items = query.all()
                  items_with_category_name.extend({
                        'user_id': item.user_id,
                        'created_at_time': item.created_at_time,
                        'image': item.image,
                        'id': item.id,
                        'category_id': item.category_id,
                        'cat_name': db.query(Category.name).filter(Category.id == item.category_id).scalar()
                  } for item in items)


            return items_with_category_name
    

    async def get_my_items(db: Session = Depends(get_db),current_user:dict = Depends(UserService.get_current_user)):

        user_id = current_user.get('id')
        user_items_with_categories = db.query(Item,Category).join(Category,Item.category_id == Category.id).filter(Item.user_id==user_id).all()

        current_user_items = []
        
        for item, category in user_items_with_categories:
            current_user_items.append({
            'user_id': user_id,
            'image': item.image,  
            'category_name': category.name,
            'category_id': category.id,
            'created_at_time':item.created_at_time
        })
        return current_user_items