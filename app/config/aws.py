import os
import uuid
import boto3
from botocore.client import ClientError
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile

load_dotenv()

# MinIO client
minio_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    region_name=os.getenv("MINIO_REGION", "us-east-1"),
)

BUCKET_NAME = os.getenv("MINIO_BUCKET", "uploads")

async def upload_file_to_minio(file: UploadFile, folder: str):
    """Uploads a file to MinIO and returns the file URL."""
    random_prefix = str(uuid.uuid4())
    minio_key = f"{folder}/{random_prefix}_{file.filename}"
    
    try:
        file.file.seek(0)
        minio_client.upload_fileobj(file.file, BUCKET_NAME, minio_key)
        file_url = f"{os.getenv('MINIO_PUBLIC_URL', 'http://localhost:9000')}/{BUCKET_NAME}/{minio_key}"
        return file_url
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

async def upload_and_validate_file(file: UploadFile, folder: str):
    await validate_file_size_type(file)
    return await upload_file_to_minio(file, folder)

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
