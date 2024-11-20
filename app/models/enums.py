from enum import Enum


# users.py
class UserGenderEnum(Enum):
    male = "male"
    female = "female"
    other = "other"

# charaters.py
class CharacterGenderEnum(Enum):
    male = 'male'
    female = 'female'
    other = 'other'

# chats.py
class ChatTypeEnum(Enum):
    user = 'user'
    character = 'character'

# default_images.py
class ImageGenderEnum(Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class ImageAgeGroupEnum(Enum):
    youth = 'youth'
    middle_age = 'middle_age'
    elderly = 'elderly'

class ImageEmotionEnum(Enum):
    youth = 'youth'
    middle_age = 'middle_age'
    elderly = 'elderly'

class ImageEmotionEnum(str, Enum):
    # A 그룹: 기쁨/행복/활기찬
    HAPPY = "A"
    JOY = "A"
    ENERGETIC = "A"
    
    # B 그룹: 슬픔
    SAD = "B"
    
    # C 그룹: 우울/불안
    DEPRESSED = "C"
    ANXIOUS = "C"
    
    # D 그룹: 버럭
    ANGRY = "D"
    
    # E 그룹: 따분/까칠/도도
    BORED = "E"
    GRUMPY = "E"
    ARROGANT = "E"

    @classmethod
    def get_emotion_groups(cls) -> dict[str, list[str]]:
        groups = {
            "A": ["기쁨", "행복", "활기찬"],
            "B": ["슬픔"],
            "C": ["우울", "불안"],
            "D": ["버럭"],
            "E": ["따분", "까칠", "도도"]
        }
        return groups

    @classmethod
    def get_korean_name(cls, emotion_code: str) -> list[str]:
        return cls.get_emotion_groups().get(emotion_code, [])