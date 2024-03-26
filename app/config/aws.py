import os
import uuid
import boto3
from botocore.client import ClientError
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()


s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


async def upload_item_photo(file):
    random_prefix = str(uuid.uuid4())
    s3_key = f"item_images/{random_prefix}_{file.filename}"
    try:
        file.file.seek(0)
        s3_client.upload_fileobj(file.file, os.getenv("AWS_BUCKET_NAME"), s3_key)
        s3_db_key = (
            f"https://s3.eu-central-1.amazonaws.com/giveme.kz-bucket-store/{s3_key}"
        )
        return s3_db_key

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

async def upload_needer_file(file):
    random_prefix = str(uuid.uuid4())
    s3_key = f"user_documents/{random_prefix}_{file.filename}"
    try:
        file.file.seek(0)
        s3_client.upload_fileobj(file.file,os.getenv('AWS_BUCKET_NAME'),s3_key)
        s3_db_key = (
            f"https://s3.eu-central-1.amazonaws.com/giveme.kz-bucket-store/{s3_key}"
        )
        return s3_db_key
    except ClientError as e:
        raise HTTPException(status_code=500,detail=f'Failed to upload files: {str(e)}')
