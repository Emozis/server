from pathlib import Path
import textwrap
import tomli

class SwaggerConfig:
    def __init__(self):
        self.title = "EMOG!"
        self.version = self._set_version_from_poetry()
        self.description = textwrap.dedent("""\
            #### 기능 목록:

            * **Auth** (_completely implemented_).
            * **User** (_completely implemented_).
            * **Characters** (_not implemented_).
            * **Default image** (_completely implemented_).
            * **Relationship** (_completely implemented_).
            * **Chat** (_completely implemented_).
            * **Chat log** (_completely implemented_).
            * **Health** (_completely implemented_).
            
            #### 문서:
                                           
            [API 변경 사항 (v0.1.0)](/docs/change_log_(0.1.0).html)
        """)
        self.tags_metadata = [
            {
                "name": "Auth",
                "description": "로그인과 권한 관련 API입니다.",
            },
            {
                "name": "User",
                "description": "유저 관련 API입니다."
            },
            {
                "name": "Character",
                "description": "캐릭터 관련 API입니다."
            },
            {
                "name": "Default image",
                "description": "기본 캐릭터 이미지 관련 API입니다."
            },
            {
                "name": "Relationship",
                "description": "캐릭터와 유저 사이의 관계에 관한 API입니다."
            },
            {
                "name": "Chat",
                "description": "채팅방 관련 API입니다."
            },
            {
                "name": "Chat log",
                "description": "채팅 기록에 관한 API입니다."
            },
            {
                "name": "Health",
                "description": "서버 상태 확인을 위한 health check API입니다."
            },
            {
                "name": "Pages",
                "description": "관리자 페이지를 위한 API입니다."
            },
        ]

    def _set_version_from_poetry(self):
        try:
            pyproject_path = Path("pyproject.toml")
            with open(pyproject_path, "rb") as f:
                pyproject = tomli.load(f)
            return pyproject["tool"]["poetry"]["version"]
        except Exception:
            return "0.0.1"

    def get_config(self):
        return {
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "tags_metadata": self.tags_metadata,
        }
    
swagger_config = SwaggerConfig()