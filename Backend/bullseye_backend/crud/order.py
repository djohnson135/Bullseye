from fastapi import Depends
from bullseye_backend.dependencies import get_db
import bullseye_backend.schemas.order as schema
import bullseye_backend.models.order as model
import json
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

async def get_user_order(current_email: str, order_num: int, db: Session):
    order = db.query(model.Order).filter_by(email = current_email, order_num = order_num).first()
    json_compatible_data = jsonable_encoder(order)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return JSONResponse(content=json_compatible_data)

async def create_order(order: schema.CreateOrder, db: Session):
    maxOrderId = db.query(func.max(model.Order.order_num)).scalar()
    if (maxOrderId is None):
        maxOrderId = 0
    else:
        maxOrderId = maxOrderId + 1
    newOrder = model.Order(**order.dict())
    newOrder.order_num = maxOrderId
    db.add(newOrder)
    db.commit()
    db.refresh(newOrder)
    return JSONResponse(content=jsonable_encoder(newOrder))

async def get_all_user_orders(current_email: str, db: Session):
    orders = db.query(model.Order).filter_by(email = current_email).all()
    json_compatible_data = jsonable_encoder(orders)
    if orders is None:
        raise HTTPException(status_code=404, detail="User has no Orders")
    return JSONResponse(content=json_compatible_data)

async def delete_order(current_email: str, order_num: int, db: Session):
    order = db.query(model.Order).filter_by(email = current_email, order_num = order_num).delete()
    if order == 0:
        raise HTTPException(status_code=404, detail= str(order_num) + " Order number does not exist")
    db.commit()

async def get_most_recent_order(current_email: str, db: Session):
    maxOrderId = db.query(func.max(model.Order.order_num)).filter_by(email = current_email).scalar()
    if (maxOrderId is None):
        raise HTTPException(status_code=404, detail="Order not found")
    order = db.query(model.Order).filter_by(email = current_email, order_num = maxOrderId).first()
    json_compatible_data = jsonable_encoder(order)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return JSONResponse(content=json_compatible_data)

async def put_order(current_email: str, order_num: int, ailse_order: schema.PutAisleOrder, db: Session):
    order = db.query(model.Order).filter_by(email = current_email, order_num = order_num).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    order_data = ailse_order.dict(exclude_unset=True)
    for key, value in order_data.items():
            setattr(order, key, value)
    json_compatible_data = jsonable_encoder(order)
    db.add(order)
    db.commit()
    db.refresh(order)
    return JSONResponse(content=json_compatible_data)