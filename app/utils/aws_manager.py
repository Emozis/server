from fastapi import UploadFile
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
import os, uuid

from ..core import logger


class AWSManager:
    def __init__(self):
        self.region_name = "ap-northeast-2"
        self.secret_name = "/prod/emogi/env"
        self.bucket_name = "emogi-bucket-2024"

        self.secrets_client = boto3.client('secretsmanager', region_name=self.region_name)
        self.s3_client = boto3.client('s3', region_name=self.region_name)

    def get_secret(self) -> Dict[str, Any]:
        """
        Secrets Manager에서 시크릿 값을 가져옵니다.
        """
        response = self.secrets_client.get_secret_value(SecretId=self.secret_name)
        if 'SecretString' in response:
            return response['SecretString']
        
    async def upload_to_s3(self, file: UploadFile, folder_path: str = "") -> bool:
        """
        S3에 파일을 업로드합니다.
        """
        folder_path = folder_path.strip('/')
        if folder_path and not folder_path.endswith('/'):
            folder_path += '/'

        file_extension = os.path.splitext(file.filename)[1]
        object_name = f"{folder_path}{uuid.uuid4()}{file_extension}"

        try:
            file_contents = await file.read()
            self.s3_client.put_object(Bucket=self.bucket_name, Key=object_name, Body=file_contents)
            logger.info(f"✅ File '{file.filename}' uploaded successfully with key '{object_name}'.")
            return object_name
        except ClientError as e:
            logger.error(f"❌ Upload failed: {str(e)}")
            return False
        
aws_managers = AWSManager()