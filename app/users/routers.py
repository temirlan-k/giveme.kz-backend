from typing import Dict, List
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    File,
    Query,
    Header,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.auth.auth_bearer import JWTBearer
from app.config.db import get_db
from app.users.schemas import (
    ChangePassword,
    CurrentUserOut,
    ResetForgetPassword,
    UserCreate,
    UserLogin,
    ForgetPasswordRequest,
)
from app.users.service import UserService, UserDocumentsService

router = APIRouter(prefix="/user")


@router.post("/signup", tags=["auth"])
async def signup(user_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    return await UserService.create_user(user_data, db)


@router.post("/login", tags=["auth"])
async def login(login_dto: UserLogin = Body(...), db: Session = Depends(get_db)):
    return await UserService.login_user(login_dto, db)


@router.get("/activate_account/", tags=["auth"])
async def activate_account(token: str = Header(None), db: Session = Depends(get_db)):
    return await UserService.activate_account(token, db)


@router.post("/forget_password", tags=["auth"])
async def forget_password(
    email: ForgetPasswordRequest = Body(...), db: Session = Depends(get_db)
):
    return await UserService.forget_password(email, db)


@router.post("/reset_password/", tags=["auth"])
async def reset_password(
    token: str = Header(None),
    rfp: ResetForgetPassword = Body(...),
    db: Session = Depends(get_db),
):
    return await UserService.reset_password(token, rfp, db)

@router.patch('/change_password',tags=['auth'])
async def change_password(password_dto: ChangePassword = Body(...), db: Session = Depends(get_db),current_user: dict = Depends(UserService.get_current_user)):
    return await UserService.change_password(password_dto,db,current_user)


@router.get("/me", dependencies=[Depends(JWTBearer())], tags=["users"])
async def read_current_user(
    current_user: CurrentUserOut = Depends(UserService.get_current_user),
):
    return current_user


@router.post('/needer_files/upload', dependencies=[Depends(JWTBearer())], tags=['users'])
async def upload_needer_files(
    electronic_doc: UploadFile = File(...),
    benefit_doc: UploadFile = File(...),
    user_photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(UserService.get_current_user)
):
    return await UserDocumentsService.upload_documents(
        electronic_doc=electronic_doc,
        benefit_doc=benefit_doc,
        user_photo=user_photo,
        db=db,
        current_user=current_user
    )
