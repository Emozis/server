from passlib.context import CryptContext

class PasswordHasher:
    def __init__(self):
        # bcrypt 알고리즘을 사용하도록 설정
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """비밀번호를 해시화합니다."""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """평문 비밀번호와 해시된 비밀번호가 일치하는지 확인합니다."""
        return self.pwd_context.verify(plain_password, hashed_password)

# 싱글톤 인스턴스 생성
password_hasher = PasswordHasher()