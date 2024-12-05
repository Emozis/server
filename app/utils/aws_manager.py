import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any


class AWSManager:
    def __init__(self):
        self.region_name = "ap-northeast-2"
        self.secret_name = "/prod/emogi/env"

        self.secrets_client = boto3.client('secretsmanager', region_name=self.region_name)
        self.s3_client = boto3.client('s3', region_name=self.region_name)

    def get_secret(self) -> Dict[str, Any]:
        """
        Secrets Manager에서 시크릿 값을 가져옵니다.
        """
        response = self.secrets_client.get_secret_value(SecretId=self.secret_name)
        if 'SecretString' in response:
            return response['SecretString']
        
aws_managers = AWSManager()