
import boto3
import uuid
from decouple import config

AWS_ACCESS_KEY=config("AWS_ACCESS_KEY",cast=str)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY",cast=str)
AWS_BUCKET_NAME=config("AWS_BUCKET_NAME",cast=str)
AWS_REGION=config("AWS_REGION",cast=str)

class S3Uploader:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key):
        self.s3 = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    async def upload_item_file(self, item_file):
        random_prefix = str(uuid.uuid4())
        file_content = await item_file.read()
        s3_key = f'item_images/{random_prefix}_{item_file.filename}'
        self.s3.put_object(Bucket='giveme.kz-bucket-store', Key=s3_key, Body=file_content)
        s3_db_key = f"https://s3.eu-central-1.amazonaws.com/giveme.kz-bucket-store/{s3_key}"
        return s3_db_key