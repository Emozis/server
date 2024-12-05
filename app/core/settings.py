from pydantic_settings import BaseSettings
from pydantic import ConfigDict, ValidationError
from typing import Optional, Dict
from botocore.exceptions import ClientError
from pathlib import Path
import boto3
import json

from . import logger

class Settings(BaseSettings):
    # DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # GOOGLE LOGIN
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # S3
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION_NAME: str
    S3_BUCKET_NAME: str

    # GEMINI
    GOOGLE_API_KEY: str
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

    @staticmethod
    def parse_env_string(env_string: str) -> Dict[str, str]:
        """환경 변수 형식의 문자열을 파싱하여 딕셔너리로 변환합니다."""
        result = {}
        lines = [line.strip() for line in env_string.split('\n') 
                if line.strip() and not line.strip().startswith('#')]
        
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
                
        return result

    @classmethod
    def get_aws_secrets(cls, secret_name: str, region_name: str) -> Optional[Dict]:
        """AWS Secrets Manager에서 설정값을 가져옵니다."""
        try:
            session = boto3.session.Session()
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name
            )
            
            response = client.get_secret_value(SecretId=secret_name)
            secret_string = response['SecretString']

            return cls.parse_env_string(json.loads(secret_string))
            
        except ClientError as e:
            logger.error(f"❌ Error fetching AWS secrets: {str(e)}")
            return None

    @classmethod
    def load_and_validate(cls, 
                         aws_secret_name: str = "/prod/emogi/env",
                         aws_region: str = "ap-northeast-2"):
        """설정을 로드하고 검증합니다. .env 파일이 없으면 AWS Secrets Manager를 사용합니다."""
        try:
            # 먼저 .env 파일에서 로드 시도
            if Path(".env").exists():
                settings = cls()
                logger.info("✅ Settings loaded successfully from .env file.")
                return settings
            
            # .env 파일이 없으면 AWS Secrets에서 로드
            logger.info("'.env' file not found, attempting to load from AWS Secrets Manager...")
            secrets = cls.get_aws_secrets(aws_secret_name, aws_region)
            
            if secrets is None:
                raise ValueError("Failed to load settings from both .env and AWS Secrets Manager")

            # AWS Secrets의 값들을 환경변수처럼 처리하기 위해 바로 Settings 인스턴스 생성
            settings = cls(**secrets)
            logger.info("✅ Settings loaded successfully from AWS Secrets Manager.")
            return settings

        except ValidationError as e:
            logger.error("❌ Error validating settings:")
            
            component_list = []
            for error in e.errors():
                loc = ".".join(str(loc) for loc in error['loc'])
                msg = error['msg']
                logger.error(f" - {loc}: {msg}")
                component_list.append(f"- `{loc}`: {msg}")
            
            raise e
        except Exception as e:
            logger.error(f"❌ Unexpected error loading settings: {str(e)}")
            raise e


try:
    settings = Settings.load_and_validate()
except Exception as e:
    logger.error("Failed to initialize settings")
    e.with_traceback()
    settings = None