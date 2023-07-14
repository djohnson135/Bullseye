from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, ARRAY, JSON
import sqlalchemy
from sqlalchemy.orm import relationship
from bullseye_backend.database import Base
from sqlalchemy.dialects.postgresql import JSONB, insert

metadata = sqlalchemy.MetaData()

class Order(Base):
    __tablename__ = "Order"
    id = Column(
        Integer, primary_key=True, index=True
    )
    store_id = Column(Integer)
    email = Column(String)
    items = Column(JSON)
    order_num = Column(Integer)
    ailse_order = Column(ARRAY(String))

