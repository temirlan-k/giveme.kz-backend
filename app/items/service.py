from typing import List
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
from app.config.aws import upload_item_photo
from app.config.db import get_db
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

    async def get_items_by_category(
        category_names: List[str] = None, db: Session = Depends(get_db)
    ):
        items_with_category_name = []

        if category_names is None:
            items = db.query(Item).all()
        else:
            for category_name in category_names:
                category = (
                    db.query(Category)
                    .filter(Category.name == category_name.upper())
                    .first()
                )

            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category {category_name} Not Found",
                )

            items = db.query(Item).filter(Item.category_id == category.id).all()
            for item in items:
                item_dict = item.__dict__
                item_dict["category_name"] = category_name
                items_with_category_name.append(item_dict)

        return items_with_category_name
