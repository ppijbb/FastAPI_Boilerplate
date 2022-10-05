from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import Header, Cookie, Body, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.db.schemas import UserInfoSchema
from app.db import crud
from main import database as Database

INDEX = APIRouter(prefix="/data",
                  tags=["crud"]
                  )


@INDEX.get(path="/",
           description="root path",
           status_code=status.HTTP_200_OK)
async def root_path():
    return "테스트 메세지"


@INDEX.get(path="/crud",
           description="DB Read test",
           status_code=status.HTTP_200_OK,
           tags=["crud"])
async def test_read(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.read(seq=query.seq,
                       email=query.email,
                       db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test select call"


@INDEX.put(path="/crud",
           description="DB Update test",
           status_code=status.HTTP_200_OK,
           tags=["crud"])
async def test_update(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.update(seq=query.seq,
                         email=query.email,
                         db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test update call"


@INDEX.post(path="/crud",
            description="DB Create test",
            status_code=status.HTTP_201_CREATED,
            tags=["crud"])
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


@INDEX.delete(path="/crud",
              description="DB Delete test",
              status_code=status.HTTP_202_ACCEPTED,
              tags=["crud"])
async def test_delete(
        query: UserInfoSchema = Depends(UserInfoSchema),
        header: Optional[str] = Header(default=None),
        body: Optional[UserInfoSchema] = Body(default=None),
        cookie: Optional[str] = Cookie(default=None),
        db_sess: Session = Depends(Database.get_db_session)
):
    result = crud.delete(seq=query.seq,
                         email=query.email,
                         db_sess=db_sess)
    print(result.DATE_STORE,
          result.BDISUM)
    return "test delete call"
