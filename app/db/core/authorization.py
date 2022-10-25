from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union, Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from fastapi import Depends, HTTPException, status
from app.db.schemas import UserLogin, TokenData, UserPassword
from app.db.models import UserInfo
from main import database as Database

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "1111@test.net",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    },
    "1111@test.net": {
        "username": "브라이언",
        "email": "1111@test.net",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    },
}

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")
auth = OAuth2PasswordBearer(tokenUrl="/user/auth",
                            scheme_name=None,
                            scopes=None,
                            description="User Authorization verification")


def get_user(db,
             username):
    with Session(Database.engine) as db_sess:
        # db_sess: Optional[Session] = Database.get_session()
        email_list = list(fake_users_db.keys())
        #db_sess.query(UserInfo.EMAIL).filter(func.length(UserInfo.EMAIL) > 0).all()
        # db_sess.close()
    # print((username,) not in email_list)
    if username not in email_list:
        raise HTTPException(status_code=400,
                            detail="INACTIVE USER")
    return UserPassword(**db[username])


def fake_hash_password(password: str):
    return pwd_context.hash(password)


def authenticate_user(db,
                      username: str,
                      password: str):
    user = get_user(db=db,
                    username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_access_token(data: dict,
                              expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode,
                             key=SECRET_KEY,
                             algorithm=ALGORITHM)
    return encoded_jwt


async def verify_access_token(token):
    try:
        decoded_jwt = jwt.decode(token=token,
                                 key=SECRET_KEY,
                                 algorithms=[ALGORITHM])
        print(f'user:{decoded_jwt["sub"]} expire time : {decoded_jwt["exp"]} {datetime.utcnow()}')
        return decoded_jwt["sub"]
    except JWTError:
        return None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(token: str = Depends(auth)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could Not Validate Credentials...",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token=token,
                             key=SECRET_KEY,
                             algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(db=fake_users_db,
                    username=token_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Authentication credentials",
                            headers={"WWW-Authenticate": "BEARER"})
    return user


async def get_current_active_user(user: UserLogin = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=400,
                            detail="INACTIVE USER")
    return user
