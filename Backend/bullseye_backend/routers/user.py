from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ..dependencies import get_db

import bullseye_backend.crud.user as crud
import bullseye_backend.schemas.user as schema
import bullseye_backend.jwt as jwt

router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=schema.User)
async def get_logged_in_user(current_email: str = Depends(jwt.get_current_user_email), db: Session = Depends(get_db)):
    return await crud.get_user_logged_in(current_email, db)

# @router.get("/{user_id}", response_model=schema.User)
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     return await crud.get_user(user_id = user_id, db=db)


# @router.get("/", response_model=List[schema.User])
# async def get_all_users(db: Session = Depends(get_db)):
#     return await crud.get_all_users(db=db)


@router.post("/", response_model=schema.UserCreate)
async def post_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(user=user, db=db)


# @router.delete("/{user_id}", status_code=204)
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     await crud.delete_user(user_id=user_id, db=db)
#     return {"Message", "Successfully Deleted"}

# @router.put("/{user_id}", status_code=200)
# async def update_user(user_id: int, user: schema.UserCreate, db: Session = Depends(get_db)):
#     await crud.update_user(user_id=user_id, user=user, db=db)
#     return {"Message", "Successfully Updated"}
