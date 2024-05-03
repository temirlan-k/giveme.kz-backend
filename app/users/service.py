from typing import List
from fastapi.responses import JSONResponse
import jwt
from sqlalchemy.orm import Session
from fastapi import Body, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import func

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import ALGORITHM, SECRET_KEY, decodeJWT, signJWT
from app.auth.email import (
    decode_reset_password_token,
    forget_password_request,
    send_verification_email,
)
from app.config.aws import upload_needer_file
from app.config.db import get_db
from app.items.models import Item
from app.items.utils import validate_file_size_type
from app.users.models import User, UserNeederDocuments
from app.users.schemas import (
    ChangePassword,
    ForgetPasswordRequest,
    ResetForgetPassword,
    UserCreate,
    UserLogin,
)
from app.users.factory.user_facroty import UserFactory
from app.users.utils import Hash, upload_and_validate_file
from validate_email import validate_email


class UserService:

    async def create_user(user_dto: UserCreate, db: Session = Depends(get_db)):

        user = db.query(User).filter(User.email == user_dto.email).first()
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        new_user = User(
            name=user_dto.name,
            surname=user_dto.surname,
            email=user_dto.email,
            password_hash=Hash.hash_password(user_dto.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_email = str(new_user.email)
        await send_verification_email(user_email, str(new_user.id))
        return signJWT(user_email)

    async def login_user(login_dto: UserLogin, db: Session = Depends(get_db)) -> str:
        user = db.query(User).filter(User.email == login_dto.email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        UserFactory._check_user_password(user, login_dto.password)
        user_email = str(user.email)
        return signJWT(user_email)

    async def activate_account(token: str, db: Session = Depends(get_db)) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id", None)
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User ID not found in token",
                )

            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            if user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already verified",
                )

            user.is_active = True
            db.commit()
            return {"message": "User account activated"}

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Expired Token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid Token")

    async def forget_password(
        fpr: ForgetPasswordRequest, db: Session = Depends(get_db)
    ):
        user = db.query(User).filter(User.email == fpr.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        forget_password_request(str(user.email))
        return {
            "success": True,
            "status_code": 200,
            "msg": f"Email has been sent to {str(fpr.email)}",
        }

    async def reset_password(
        token: str,
        rfp_data: ResetForgetPassword = Body(...),
        db: Session = Depends(get_db),
    ):
        try:
            token_info = await decode_reset_password_token(token)
            print(token_info)
            if token_info is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token"
                )

            user_email = token_info.get("email")
            if user_email is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Email not found in token",
                )

            user = db.query(User).filter(User.email == user_email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            new_hashed_password = Hash.hash_password(rfp_data.new_password)
            user.password_hash = new_hashed_password
            db.add(user)
            db.commit()
            return {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Password reset successful!",
            }

        except HTTPException as http_exception:
            raise http_exception
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something unexpected happened!",
            )



    async def get_current_user(
        token: str = Depends(JWTBearer()), db: Session = Depends(get_db)
    ):

        payload = decodeJWT(token)
        user_email = payload.get("email")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token"
            )

        user = db.query(User).filter(User.email == user_email).first()
        total_bonuses = db.query(func.sum(Item.bonus)).filter(Item.user_id == user.id).scalar() or 0 
        needer_status = db.query(UserNeederDocuments.status).filter(UserNeederDocuments.user_id == user.id).first()
        if needer_status is not None:
            needer_status = [status.name for status in needer_status]
            print(needer_status[0])
        

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user = {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "is_active": user.is_active,
            "is_needer": user.is_needer,
            "role": user.role,
            "bar_code":user.bar_code,
            "bonus_count":total_bonuses,
            "needer_status":needer_status[0] if needer_status else 'NULL',
        }
        return user
    

    async def change_password(passwords_dto:ChangePassword,db:Session=Depends(get_db),current_user:dict = Depends(get_current_user)):
        user = db.query(User).filter(User.id==current_user.get('id')).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
        
        if not Hash.verify_password(passwords_dto.old_password,user.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password,try again")

        user.password_hash = Hash.hash_password(passwords_dto.new_password)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content={
        'success': True,
        "status_code": status.HTTP_200_OK,
        'msg': 'Password changed'
        })
            
 

        





class UserDocumentsService:
    

    async def upload_documents(electronic_doc: UploadFile, benefit_doc: UploadFile, user_photo: UploadFile, db: Session, current_user: dict):

        if not all([electronic_doc, benefit_doc, user_photo]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You must upload all 3 files')
        user = db.query(UserNeederDocuments).filter(UserNeederDocuments.user_id==current_user.get('id')).first()
        if user:
            raise HTTPException(status_code=400,detail='You already uploaded files')

        electronic_id_url = await upload_and_validate_file(electronic_doc)
        benefit_document_url = await upload_and_validate_file(benefit_doc)
        user_photo_url = await upload_and_validate_file(user_photo)

        db_needer_file = UserNeederDocuments(
            user_id=current_user.get('id'),
            electronic_id=electronic_id_url,
            benefit_document=benefit_document_url,
            user_photo=user_photo_url,
        )

        db.add(db_needer_file)
        db.commit()

        success_response = {
            'success': True,
            'user': current_user.get('id')
        }
        return success_response
