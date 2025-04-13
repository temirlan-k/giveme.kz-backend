import os
import shutil
import uuid
import boto3
from botocore.client import ClientError
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile

from app.items.utils import validate_file_size_type

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://givemekz-backend-production.up.railway.app")  # фронту отдаём полный путь
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# MinIO client
minio_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    region_name=os.getenv("MINIO_REGION", "us-east-1"),
)


async def save_file_locally(file: UploadFile, folder: str) -> str:
    """Save uploaded file to uploads/<folder>/ and return public URL."""
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4()}{ext}"
    
    folder_path = os.path.join(UPLOAD_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return f"{BASE_URL}/uploads/{folder}/{filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


async def upload_and_validate_file(file: UploadFile, folder: str):
    await validate_file_size_type(file)
    return await save_file_locally(file, folder)


async def upload_needer_documents(electronic_doc: UploadFile, benefit_doc: UploadFile, user_photo: UploadFile):
    """Uploads multiple user documents to MinIO."""
    if not all([electronic_doc, benefit_doc, user_photo]):
        raise HTTPException(status_code=400, detail="You must upload all 3 files")
    
    electronic_doc_url = await upload_and_validate_file(electronic_doc, "user_documents")
    benefit_doc_url = await upload_and_validate_file(benefit_doc, "user_documents")
    user_photo_url = await upload_and_validate_file(user_photo, "user_photos")
    
    return {
        "success": True,
        "electronic_doc": electronic_doc_url,
        "benefit_doc": benefit_doc_url,
        "user_photo": user_photo_url,
    }


