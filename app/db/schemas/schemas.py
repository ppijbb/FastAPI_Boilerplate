from typing import Union
from pydantic import BaseModel


# 이메일 기준 유저 정보 Query
class UserInfoSchema(BaseModel):
    seq: int
    email: str


# fastAPI 문서 예제 Request Body 모델
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


# 테스트 보안 토큰
class SecurityToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserLogin(BaseModel):
    username: str
    email: Union[str, None] = None


class UserPassword(UserLogin):
    hashed_password: str
