from pydantic import BaseModel, Field, Json, parse_obj_as
from enum import Enum
from typing import TypeVar, Generic, Type, Any, Dict
from abc import ABC

class Item(str, Enum):
    tcin = 'tcin'
    name = 'name'
    aisle = 'aisle'
    image = 'image'

class OrderBase(BaseModel):
    email: str
    

class CreateOrder(OrderBase):
    items: list[Dict[str, str]] = None
    # items: Json
    store_id: int
    
    class Config:
        orm_mode = True

class PutAisleOrder(BaseModel):
    ailse_order: list[str]
    class Confgi:
        orm_mode = True

class Order(OrderBase):
    items: list[Dict[str, str]] = None
    store_id: int
    order_num: int

    class Config:
        orm_mode = True