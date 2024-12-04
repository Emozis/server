import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from app.database.base import Base
from app.core import logger, settings


# .env.test 파일 로드
load_dotenv('.env.test')

class DatabaseManagerForTest:
    def __init__(self):
        self.host = settings.POSTGRES_HOST
        self.port = settings.POSTGRES_PORT
        self.db_name = f"{settings.POSTGRES_DB}_test"  # 테스트 DB 이름에 _test 접미사 추가
        self.user = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD

        self.Base = Base
        self.engine = None
        self.SessionLocal = None
        self.DATABASE_URL = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    def create_database(self):
        """테스트 데이터베이스 생성"""
        try:
            # postgres 기본 데이터베이스에 연결
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # 데이터베이스 존재 여부 확인
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.db_name}'")
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f"CREATE DATABASE {self.db_name}")

            return True

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def setup_database(self):
        """데이터베이스 연결 설정"""
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # 테이블 생성
        self.Base.metadata.create_all(bind=self.engine)
        return self.engine, self.SessionLocal

    def drop_database(self):
        """테스트 데이터베이스 삭제"""
        try:
            # 먼저 모든 연결 종료
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database="postgres"
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # 현재 연결된 세션 강제 종료
            cursor.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{self.db_name}'
                AND pid <> pg_backend_pid();
            """)
            
            # 데이터베이스 삭제
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def execute_sql_files(self, sql_directory):
        """지정된 디렉토리의 SQL 파일들을 실행"""
        try:
            if not os.path.exists(sql_directory):
                logger.warning(f"⚠️ Test SQL directory not found: {sql_directory}")
                return False

            sql_files = sorted([f for f in os.listdir(sql_directory) if f.endswith('.sql')])
            
            if not sql_files:
                logger.warning(f"⚠️ No SQL files found in {sql_directory}")
                return False

            logger.info(f"🔄 Executing {len(sql_files)} SQL files for test data")
            
            with self.engine.connect() as conn:
                for sql_file in sql_files:
                    file_path = os.path.join(sql_directory, sql_file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            sql_content = f.read()

                        if sql_content.strip():
                            conn.execute(text(sql_content))
                            conn.commit()
                            logger.info(f"   ✅ Executed {sql_file}")
                        else:
                            logger.warning(f"   ⚠️ Skipped empty file: {sql_file}")

                    except Exception as e:
                        logger.error(f"   ❌ Error executing {sql_file}: {str(e)}")
                        continue

            logger.info("✅ Test SQL files execution completed")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to execute test SQL files: {str(e)}")
            return False