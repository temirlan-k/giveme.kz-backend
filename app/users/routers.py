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


@router.post("/activate_account/", tags=["auth"])
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


@router.get("/me", dependencies=[Depends(JWTBearer())], tags=["users"])
async def read_current_user(
    current_user: CurrentUserOut = Depends(UserService.get_current_user),
):
    return current_user


@router.post('/needer_files/upload',dependencies=[Depends(JWTBearer())],tags=['users'])
async def upload_needer_files(files: List[UploadFile] = File(...),db : Session = Depends(get_db),current_user:dict = Depends(UserService.get_current_user)):
    return await UserDocumentsService.upload_documents(files,db,current_user)

