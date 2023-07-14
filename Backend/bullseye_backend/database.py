from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from bullseye_backend.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # create sessionlocal class using sessionmaker function


Base = declarative_base()  # create a base class


def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)