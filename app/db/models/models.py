from sqlalchemy import (Column, Integer, String, JSON, DateTime,
                        FLOAT, SmallInteger, PrimaryKeyConstraint, ForeignKey)
import datetime as dt
from typing import Union, Optional
from app.db.core.database import Base


class UserInfo(Base):
    __tablename__ = "pperson"

    EP: Union[str, Column] = Column(String(10), primary_key=True)
    EPNAME: Union[str, Column] = Column(String(20))
    LASTBDI_STORE: Union[int, Column] = Column(SmallInteger)
    SEQ_Q: Union[int, Column] = Column(SmallInteger)
    FACTOR_SEQ: Union[int, Column] = Column(SmallInteger)
    FACTOR_NO: Union[int, Column] = Column(SmallInteger)
    DATE_STORE: Union[str, Column] = Column(DateTime)
    EMAIL: Union[str, Column] = Column(String(50), primary_key=True)
    AGE: Union[int, Column] = Column(SmallInteger)
    GENDER: Union[int, Column] = Column(SmallInteger)
    D_NAME: Union[str, Column] = Column(String(32))

    def __init__(
            self,
            ep,
            epname,
            lastbdi_store,
            seq_q,
            factor_seq,
            factor_no,
            email,
            age,
            gender
    ):
        self.EP = ep
        self.EPNAME = epname
        self.LASTBDI_STORE = lastbdi_store
        self.SEQ_Q = seq_q
        self.FACTOR_SEQ = factor_seq
        self.FACTOR_NO = factor_no
        self.DATE_STORE = dt.datetime.now()
        self.EMAIL = email
        self.AGE = age
        self.GENDER = gender
        self.D_NAME = "test"

    def __repr__(self):
        return "<UserInfo('%s', '%s', '%d', '%d', '%d', '%d', '%s', '%s', '%d', '%d')>" \
               % (self.EP, self.EPNAME, self.LASTBDI_STORE, self.SEQ_Q, self.FACTOR_SEQ, self.FACTOR_NO,
                  self.DATE_STORE, self.EMAIL, self.AGE, self.GENDER)


class TestTable(Base):
    __tablename__ = 'Table'
    EP = Column(ForeignKey("pperson.EP"))
    DATE_STORE = Column(DateTime)
    SEQ_Q = Column(SmallInteger)
    FACEFILE = Column(DateTime)
    EMOTION = Column(SmallInteger)
    D_NAME = Column(String(32))
    TEST01 = Column(SmallInteger)
    TEST02 = Column(SmallInteger)
    TEST03 = Column(SmallInteger)
    TEST04 = Column(SmallInteger)
    TEST05 = Column(SmallInteger)
    TESTSUM = Column(SmallInteger)
    DESCRIPTION = Column(String(128))

    __table_args__ = (
        PrimaryKeyConstraint(EP, SEQ_Q),
        {},
    )

    class Config:
        orm_mode = True

    @staticmethod
    def get_new_record(ep,
                       seq=None):
        seq = seq if seq else 1
        return [ep, seq, "test", dt.datetime.now()] + [None] * 5 + ["진행중"]

    def __init__(
            self,
            ep,
            seq,
            d_name,
            facefile,
            test01,
            test02,
            test03,
            test04,
            test05,
            testsum,
            description
    ):
        self.EP = ep
        self.SEQ_Q = seq
        self.DATE_STORE = dt.datetime.now()
        self.FACEFILE = facefile
        self.EMOTION = 1
        self.D_NAME = d_name

        self.TEST01 = test01
        self.TEST02 = test02
        self.TEST03 = test03
        self.TEST04 = test04
        self.TEST05 = test05
        self.BDISUM = testsum
        self.DESCRIPTION = description

    def __repr__(self):
        return "<TESTTABLE(" \
               "'%s', '%s', '%d', '%s','%d','%s', " \
               "'%d', '%d', '%d', '%d', '%d', " \
               "'%d', " \
               "'%s')>" \
               % (self.EP, self.DATE_STORE, self.SEQ_Q, self.FACEFILE, self.EMOTION, self.D_NAME,
                  self.TEST01, self.TEST02, self.TEST03, self.TEST04, self.TEST05, self.TESTSUM,
                  self.DESCRIPTION)

    def _none_check(self,):
        seq_list = [self.TEST01, self.TEST02, self.TEST03, self.TEST04, self.TEST05]

        if seq_list.count(None) == 0:
            return True, seq_list
        elif None in seq_list:
            return False, seq_list

