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