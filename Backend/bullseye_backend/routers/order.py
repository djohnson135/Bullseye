from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ..dependencies import get_db

import bullseye_backend.crud.order as crud
import bullseye_backend.schemas.order as schema
import bullseye_backend.jwt as jwt


router = APIRouter(
    prefix="/order",
    tags=["order"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)



@router.get("/recent")
async def get_recent_order(current_email: str = Depends(jwt.get_current_user_email), db: Session = Depends(get_db)):
    return await crud.get_most_recent_order(current_email, db)

# @router.get("/{current_email}")
# async def get_all_user_orders(current_email: str, db: Session = Depends(get_db)):
#     return await crud.get_all_user_orders(current_email, db)

@router.post("/")
async def post_order(order: schema.CreateOrder, db: Session = Depends(get_db)):
    return await crud.create_order(order=order, db=db)

@router.delete("/{order_num}", status_code=204)
async def delete_order( order_num: int, current_email: str = Depends(jwt.get_current_user_email), db: Session = Depends(get_db)):
    await crud.delete_order(current_email, order_num, db)
    return {"Message", "Successfully Deleted"}

@router.patch("/{current_email}/{order_num}", status_code=204)
async def put_order( current_email: str, order_num: int, ailse_order: schema.PutAisleOrder, db: Session = Depends(get_db)):
    return await crud.put_order(current_email, order_num, ailse_order, db)