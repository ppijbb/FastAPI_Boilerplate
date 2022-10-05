from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import Header, Cookie, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from datetime import timedelta
# from main import database as Database
from app.db.schemas import UserInfoSchema
from app.db import crud
from app.db.core.authorization import (get_current_active_user,
                                       fake_users_db,
                                       authenticate_user,
                                       create_access_token,
                                       ACCESS_TOKEN_EXPIRE_MINUTES)

USER = APIRouter(prefix="/user",
                 tags=["user"])
templates = Jinja2Templates(directory="app/templates")


# @USER.get(path="/",
#           description="root path",
#           status_code=status.HTTP_200_OK)
# async def root_path():
#     return "테스트 메세지"


@USER.get(path="/signin",
          description="DB User Info Read test",
          # summary="read user data",
          # response_description="test output",
          status_code=status.HTTP_200_OK,
          tags=None)
async def test_read(
        request: Request,
        # query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session),
):
    # result = crud.read(seq=query.seq,
    #                    email=query.email,
    #                    db_sess=db_sess)
    # print(result.DATE_STORE,
    #       result.BDISUM)
    return templates.TemplateResponse(name="login.html",
                                      context={"request": request})


@USER.post(path="/auth",
           description="User Authorization api",
           deprecated=True)
async def login(request: Request,
                form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db=fake_users_db,
                             username=form_data.username,
                             password=form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail="ID Verification Error",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    # {
    #     "user_name": user.username,
    #     "access_token": access_token,
    #     "token_type": "bearer"
    # }
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token",
                        value=access_token,
                        httponly=True)
    return response


@USER.put(path="/update",
          description="DB User Info Update test",
          status_code=status.HTTP_200_OK,
          tags=None)
async def test_update(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session),
        token: str = Depends(get_current_active_user),
):
    print(token)
    result = crud.update(seq=query.seq,
                         email=query.email,
                         db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return {"result": "success",
            "user": token.username}


@USER.patch(path="/patch",
            description="DB User Info Patch test",
            status_code=status.HTTP_200_OK,
            tags=None)
async def test_options(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.read(seq=query.seq,
                       email=query.email,
                       db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test patch call"


@USER.post(path="/signup",
           description="DB User Info Create test",
           status_code=status.HTTP_201_CREATED,
           tags=None)
async def test_create(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.create(seq=query.seq,
                         email=query.email,
                         db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test insert call"


@USER.delete(path="/delete",
             description="DB User Info Delete test",
             status_code=status.HTTP_202_ACCEPTED,
             tags=None)
async def test_delete(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.read(seq=query.seq,
                       email=query.email,
                       db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test delete call"


@USER.head(path="/head",
           description="DB User Info Head test",
           status_code=status.HTTP_200_OK,
           tags=None)
async def test_head(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.read(seq=query.seq,
                       email=query.email,
                       db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test head call"


@USER.options(path="/options",
              description="DB User Info Options test",
              status_code=status.HTTP_200_OK,
              tags=None)
async def test_options(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.read(seq=query.seq,
                       email=query.email,
                       db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test options call"


@USER.trace(path="/trace",
            description="DB User Info Trace test",
            status_code=status.HTTP_200_OK,
            tags=None)
async def test_trace(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.read(seq=query.seq,
                       email=query.email,
                       db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test trace call"
