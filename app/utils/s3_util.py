from fastapi import UploadFile
import boto3
from botocore.exceptions import NoCredentialsError
import os
import uuid

from ..core import settings, logger

ACCESS_KEY = settings.S3_ACCESS_KEY
SECRET_KEY = settings.S3_SECRET_KEY
REGION_NAME = settings.S3_REGION_NAME
BUCKET_NAME = settings.S3_BUCKET_NAME

s3 = boto3.client('s3',
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY,
                  region_name=REGION_NAME)


async def upload_to_s3(file: UploadFile, folder_path: str = "", object_name=None):
    # folder_path 앞뒤의 '/' 제거 후 뒤에 '/'추가
    folder_path = folder_path.strip('/')
    if folder_path and not folder_path.endswith('/'):
        folder_path += '/'

    file_extension = os.path.splitext(file.filename)[1]
    unique_id = uuid.uuid4()

    if object_name is not None:
        object_name = f"{folder_path}{unique_id}_{object_name}{file_extension}"
    else:
        object_name = f"{folder_path}{unique_id}{file_extension}"

    try:
        file_contents = await file.read()
        s3.put_object(Bucket=BUCKET_NAME, Key=object_name, Body=file_contents)

        file_url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{object_name}"

        logger.info(f"✅ File '{file.filename}' uploaded successfully as '{object_name}'. URL: {file_url}")

        return file_url
    except NoCredentialsError:
        logger.error("❌ Credentials not available. Please check your AWS credentials.")
        return None
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        return None