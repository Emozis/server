# Admin Page

>Swagger url : http://13.125.66.68:8000/docs

EMOGI 관리자 페이지 관련 문서입니다.

React 사용x -> HTML, CSS, JS로 만들어 주시면 백엔드 서버에 넣을 예정



| 구분 | 화면 | 세부사항 | 비고 |
|-------|-------|-------|-------|
| 로그인 | 관리자 로그인 화면 | 아이디/패스워드 |  |
| 대쉬보드 | 관리자 대쉬보드 화면 | 내용x | 추후 구현을 위해 페이지만 할당 |
| 캐릭터 | 캐릭터 관리 화면 | 캐릭터 조회/생성/수정/삭제 |
| 이미지 | 기본 이미지 관리 화면 | 이미지 조회/생성/수정/삭제 |
| 관계 | 캐릭터-유저 관계 관리 화면 | 관계 조회/생성/수정/삭제 |

## 캐릭터

#### 캐릭터 조회
- [캐릭터 조회 api](http://13.125.66.68:8000/docs#/Character/get_public_characters_api_v1_character_get)
- 캐릭터 번호/이름/프로필 이미지/성별/성격/상세내용/관계/만든날짜/만든사람

#### 캐릭터 생성
: 관계 부분은 관계 조회 api에서 가져와서 선택하도록(유저랑 비슷함)
- [캐릭터 수정 api](http://13.125.66.68:8000/docs#/Character/create_character_api_v1_character_post)
- 캐릭터 이름/프로필 이미지/성별/성격/한줄설명/첫인사/상세내용/관계/공개여부

#### 캐릭터 수정
- [캐릭터 수정 api](http://13.125.66.68:8000/docs#/Character/update_character_api_v1_character__character_id__put)
- 생성과 동일

#### 캐릭터 삭제
- [캐릭터 삭제 api](http://13.125.66.68:8000/docs#/Character/delete_character_api_v1_character__character_id__delete)


## 기본 이미지

#### 이미지 조회
- [이미지 조회 api](http://13.125.66.68:8000/docs#/Default%20image/get_images_api_v1_default_image_get)
- 이미지 번호/이름/주소(사진을 보여줘야겠지)/성별/나이대/감정/생성날짜/수정날짜

#### 이미지 생성
- [이미지 수정 api](http://13.125.66.68:8000/docs#/Default%20image/create_default_image_api_v1_default_image_post)
- 이미지 등록/성별(select)/나이대(select)/감정(select)

#### 이미지 수정
- [이미지 수정 api](http://13.125.66.68:8000/docs#/Default%20image/update_image_api_v1_default_image__image_id__put)
- 등록과 동일

#### 이미지 삭제
- [이미지 삭제 api](http://13.125.66.68:8000/docs#/Default%20image/delete_image_api_v1_default_image__image_id__delete)


## 관계

#### 관계 조회
- [관계 조회 api](http://13.125.66.68:8000/docs#/Relationship/get_relationships_api_v1_relationship_get)
- 관계 번호/이름
- 카테고리 했던거랑 동일

#### 관계 생성
- [관계 수정 api](http://13.125.66.68:8000/docs#/Relationship/create_relationship_api_v1_relationship_post)
- 관계 이름

#### 관계 수정
- [관계 수정 api](http://13.125.66.68:8000/docs#/Relationship/update_relationship_api_v1_relationship__relationship_id__put)
- 등록과 동일

#### 관계 삭제
- [관계 삭제 api](http://13.125.66.68:8000/docs#/Relationship/delete_relationship_api_v1_relationship__relationship_id__delete)

