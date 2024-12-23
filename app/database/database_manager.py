import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

from ..core import logger, settings
from ..database.base import Base
from ..utils.constants import constants


class DatabaseManager:
    def __init__(self):
        self.host = settings.POSTGRES_HOST
        self.port = settings.POSTGRES_PORT
        self.db_name = settings.POSTGRES_DB
        self.user = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD

        self.Base = Base
        self.engine = None
        self.SessionLocal = None
        self.DATABASE_URL = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    def create_database(self):
        """데이터베이스가 없으면 생성"""
        try:
            # postgres 기본 데이터베이스에 연결
            logger.info(f"🔄 Attempting to create database '{self.db_name}'...")
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database="postgres"  # 기본 데이터베이스로 연결
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # 데이터베이스 존재 여부 확인
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.db_name}'")
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f"CREATE DATABASE {self.db_name}")
                logger.info(f"✅ Database '{self.db_name}' created successfully")
            else:
                logger.info(f"🗂️ Database '{self.db_name}' already exists")

            return True

        except Exception as e:
            logger.error(f"❌ Error creating database: {str(e)}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def _setup_connection(self):
        """데이터베이스 연결 설정 및 테스트"""
        try:
            self.engine = create_engine(
                url=self.DATABASE_URL,
                pool_size=constants.POOL_SIZE,
                max_overflow=constants.MAX_OVERFLOW,
                pool_timeout=30,
                pool_pre_ping=True,
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # 데이터베이스 연결 테스트
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            masked_url = f"postgresql://{self.user}:****@{self.host}:{self.port}/{self.db_name}"
            logger.info(f"✅ Database connection successful - Connected to {masked_url}")
            return True
        except OperationalError as e:
            self.engine = None
            self.SessionLocal = None

            logger.error(f"❌ Failed to connect to database: {str(e)}")
            return False

    def init_database(self):
        """데이터베이스 엔진 및 세션 초기화"""
        if self._setup_connection():
            return self.engine, self.SessionLocal, self.Base
        
        if self.create_database():
            if self._setup_connection():
                return self.engine, self.SessionLocal, self.Base
            else:
                raise Exception(f"Failed to connect to database '{self.db_name}' after creation")
        else:
            raise Exception(f"Failed to create database '{self.db_name}'")
            
    def create_all_tables(self):
        """SQLAlchemy 모델에 정의된 모든 테이블 생성"""
        try:
            logger.info("🔄 Creating all database tables...")

            # 테이블 생성
            self.Base.metadata.create_all(bind=self.engine)
            
            # 생성된 테이블 목록 가져오기
            inspector = inspect(self.engine)
            table_names = inspector.get_table_names()
            
            logger.info(f"✅ Successfully created {len(table_names)} tables:")
            for table in table_names:
                logger.info(f"   📋 {table}")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {str(e)}")
            return False
        
    def drop_all_tables(self, confirmation=False):
        """데이터베이스의 모든 테이블 삭제
        Args:
            confirmation (bool): 실수로 인한 삭제 방지를 위한 안전 파라미터
        """
        if not confirmation:
            logger.warning("⚠️  Table deletion requires confirmation. Set confirmation=True to proceed")
            return False
            
        try:
            logger.warning("⚠️  Dropping all database tables...")

            inspector = inspect(self.engine)
            table_names = inspector.get_table_names()
            
            # 모든 테이블 삭제
            self.Base.metadata.drop_all(bind=self.engine)
            
            logger.info(f"✅ Successfully dropped {len(table_names)} tables:")
            for table in table_names:
                logger.info(f"   🗑️  {table}")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to drop tables: {str(e)}")
            return False
        
    def execute_sql_files(self, sql_directory):
        """지정된 디렉토리의 SQL 파일들을 실행
        Args:
            sql_directory (str): SQL 파일들이 있는 디렉토리 경로
        """
        try:
            if not os.path.exists(sql_directory):
                logger.error(f"❌ SQL directory not found: {sql_directory}")
                return False

            # SQL 파일 목록 가져오기 (.sql 확장자만)
            sql_files = sorted([f for f in os.listdir(sql_directory) if f.endswith('.sql')])
            
            if not sql_files:
                logger.warning(f"⚠️ No SQL files found in {sql_directory}")
                return False

            logger.info(f"🔄 Executing {len(sql_files)} SQL files from {sql_directory}")
            
            # 각 SQL 파일 실행
            with self.engine.connect() as conn:
                for sql_file in sql_files:
                    file_path = os.path.join(sql_directory, sql_file)
                    try:
                        # SQL 파일 읽기
                        with open(file_path, 'r', encoding='utf-8') as f:
                            sql_content = f.read()

                        # SQL 문 실행
                        if sql_content.strip():  # 빈 파일이 아닌 경우만 실행
                            conn.execute(text(sql_content))
                            conn.commit()
                            logger.info(f"   ✅ Executed {sql_file}")
                        else:
                            logger.warning(f"   ⚠️ Skipped empty file: {sql_file}")

                    except Exception as e:
                        logger.error(f"   ❌ Error executing {sql_file}: {str(e)}")
                        # 개별 파일 실패 시에도 계속 진행
                        continue

            logger.info("✅ SQL files execution completed")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to execute SQL files: {str(e)}")
            return False
        

db_manager = DatabaseManager()
engine, SessionLocal, Base = db_manager.init_database()

def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션 제공"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()