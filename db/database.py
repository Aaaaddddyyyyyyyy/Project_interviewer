from sqlalchemy.orm import Session

from db.models import engine


def get_session():

    return Session(engine)