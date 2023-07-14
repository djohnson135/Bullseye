from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
import sqlalchemy
from sqlalchemy.orm import relationship
from bullseye_backend.database import Base

metadata = sqlalchemy.MetaData()

class User(Base):
    __tablename__ = "User"
    id = Column(
        Integer, primary_key=True, index=True
    )
    email = Column(String)
    lname = Column(String)
    fname = Column(String)


