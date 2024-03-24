from typing import List
import uuid
import boto3

from sqlalchemy.orm import Session
from fastapi import BackgroundTasks, Body, Depends, HTTPException, Query, Request, status,UploadFile,File
from decouple import config
from fastapi.responses import JSONResponse

from app.config.aws import S3Uploader
from app.config.db import get_db
from app.items.schemas import ItemCreate
from app.items.models import Item,Category
from app.items.utils import validate_file_size_type
from decouple import config
from app.users.service import UserService

AWS_ACCESS_KEY=config("AWS_ACCESS_KEY",cast=str)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY",cast=str)
AWS_BUCKET_NAME=config("AWS_BUCKET_NAME",cast=str)
AWS_REGION=config("AWS_REGION",cast=str)

s3_uploader = S3Uploader(AWS_REGION,AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY)


class ItemService:

      async def create_item(item_file: UploadFile = File(...),category_id: int = Body(...),
                           db: Session = Depends(get_db),current_user: str = Depends(UserService.get_current_user)):
            
            if not current_user.get('is_active',False):
                  raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only verified user can upload items. Activate your account')
            if category_id < 1 or category_id > db.query(Category).count():
                  raise HTTPException(status_code=400,detail='Error Category')
            
            await validate_file_size_type(item_file)

            s3_db_key = await s3_uploader.upload_item_file(item_file)

            new_item = Item(
                  image=s3_db_key,
                  category_id=category_id,
                  user_id=current_user.get('id')
            )
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return {'success':True,'user':current_user.get('id'),'link':s3_db_key}
      

      async def get_items_by_category(category_names: List[str] = None, db: Session = Depends(get_db)):
            items_by_category = {}

            if category_names is None:
                  return db.query(Item).all()
            
            for category_name in category_names:
                  category = db.query(Category).filter(Category.name == category_name.upper()).first()

                  if category is None:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category {category_name} Not Found')
                  
                  items = db.query(Item).filter(Item.category_id==category.id).all()
                  items_by_category[category.name] = [item for item in items]

            return items_by_category

      
                        

