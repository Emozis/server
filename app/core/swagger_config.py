import textwrap

class SwaggerConfig:
    def __init__(self):
        self.title = "eMoGi"
        self.version = "0.0.1"
        self.description = textwrap.dedent("""\
            기능 목록:

            * **Auth** (_completely implemented_).
            * **User** (_completely implemented_).
            * **Characters** (_not implemented_).
            * **Default image** (_completely implemented_).
            * **Relationship** (_completely implemented_).
            * **Chat** (_completely implemented_).
            * **Chat log** (_completely implemented_).
        """)
        self.license_info = {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        }
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
                "name": "Characters",
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
        ]

    def get_config(self):
        return {
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "license_info": self.license_info,
            "tags_metadata": self.tags_metadata,
        }
    
swagger_config = SwaggerConfig()