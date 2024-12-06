from fastapi import UploadFile
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional
import os, uuid

from ..core import logger


class AWSManager:
    def __init__(self):
        self.region_name = "ap-northeast-2"
        self.secret_name = "/prod/emogi/env"
        self.bucket_name = "emogi-bucket-2024"
        self.cloudfront_domain = "d18qrti6vmh2m5.cloudfront.net"

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

    def get_file_url(self, object_name: str, expiration: int = 3600) -> Optional[str]:
        """
        S3에 업로드된 파일의 미리 서명된 URL을 생성합니다.
        
        Args:
            object_name (str): S3 객체 키
            expiration (int): URL 만료 시간(초), 기본값 1시간
            
        Returns:
            str: 미리 서명된 URL
            None: URL 생성 실패 시
        """
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            logger.info(f"✅ Presigned URL generated for '{object_name}'")
            return response
        except ClientError as e:
            logger.error(f"❌ Failed to generate presigned URL: {str(e)}")
            return None
        
    def get_cloudfront_url(self, object_name: str) -> str:
        """
        CloudFront를 통한 파일 URL을 생성합니다.
        
        Args:
            object_name (str): S3 객체 키
            
        Returns:
            str: CloudFront URL
        """
        object_name = object_name.lstrip('/')
        return f"https://{self.cloudfront_domain}/{object_name}"
        
    def delete_files(self, object_names: list[str]) -> dict[str, bool]:
        """
        S3에서 여러 파일을 한 번에 삭제합니다.
        
        Args:
            object_names (list[str]): 삭제할 파일들의 S3 객체 키 리스트
            
        Returns:
            dict[str, bool]: 각 파일별 삭제 성공 여부
        """
        results = {}
        try:
            objects = [{'Key': name} for name in object_names]
            response = self.s3_client.delete_objects(
                Bucket=self.bucket_name,
                Delete={
                    'Objects': objects,
                    'Quiet': False
                }
            )
            
            # 성공한 삭제 처리
            if 'Deleted' in response:
                for obj in response['Deleted']:
                    results[obj['Key']] = True
                    logger.info(f"✅ File '{obj['Key']}' deleted successfully.")
            
            # 실패한 삭제 처리
            if 'Errors' in response:
                for error in response['Errors']:
                    results[error['Key']] = False
                    logger.error(f"❌ Failed to delete '{error['Key']}': {error['Message']}")
            
            return results
        
        except ClientError as e:
            logger.error(f"❌ Bulk delete failed: {str(e)}")
            return {name: False for name in object_names}
        

aws_managers = AWSManager()