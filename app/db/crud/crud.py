from sqlalchemy.orm import Session
from app.db.models import UserInfo, TestTable


def create(
        seq: int,
        email: str,
        db_sess: Session
):
    _user = db_sess.query(UserInfo) \
                   .filter(UserInfo.EMAIL == email) \
                   .first()
    return db_sess.query(TestTable) \
                  .filter(TestTable.EP == _user.EP) \
                  .order_by(TestTable.SEQ_Q.desc()) \
                  .first()


def read(
        seq: int,
        email: str,
        db_sess: Session
):
    _user = db_sess.query(UserInfo) \
                   .filter(UserInfo.EMAIL == email) \
                   .first()
    return db_sess.query(TestTable) \
                  .filter(TestTable.EP == _user.EP) \
                  .order_by(TestTable.SEQ_Q.desc()) \
                  .first()


def update(
        seq: int,
        email: str,
        db_sess: Session
):
    print("session ", db_sess)
    _user = db_sess.query(UserInfo) \
                   .filter(UserInfo.EMAIL == email) \
                   .first()
    return db_sess.query(TestTable) \
                  .filter(TestTable.EP == _user.EP) \
                  .order_by(TestTable.SEQ_Q.desc()) \
                  .first()


def delete(
        seq: int,
        email: str,
        db_sess: Session
):
    _user = db_sess.query(UserInfo) \
                   .filter(UserInfo.EMAIL == email) \
                   .first()
    return db_sess.query(TestTable) \
                  .filter(TestTable.EP == _user.EP) \
                  .order_by(TestTable.SEQ_Q.desc()) \
                  .first()
