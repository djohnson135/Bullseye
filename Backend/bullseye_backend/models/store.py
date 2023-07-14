from sqlalchemy import Column, Integer, String, MetaData, ARRAY, JSON
from bullseye_backend.database import Base

metadata = MetaData()


class Store(Base):
    __tablename__ = "Store"
    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String)
    city = Column("city", String)
    state = Column("state", String)
    zipcode = Column("zipcode", String)
    map = Column("map", ARRAY(String))
    aisles = Column("aisles", JSON)
