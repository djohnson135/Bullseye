from fastapi import Depends
from bullseye_backend.dependencies import get_db
import bullseye_backend.schemas.user as schema
import bullseye_backend.models.user as model

from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException


async def create_user(user: schema.UserCreate, db: Session):
    newUser = model.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return schema.User.from_orm(newUser)

async def get_all_users(db: Session):
    user = db.query(model.User).all()
    if user is None:
        raise HTTPException(status_code=404, detail="No users found")
    return list(map(schema.User.from_orm, user))


async def get_user(user_id: int, db: Session):
    user = db.query(model.User).filter_by(id = user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail= str(user_id) + " User does not exist")
    return schema.User.from_orm(user)

async def delete_user(user_id: int, db: Session):
    user = db.query(model.User).filter_by(id = user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail= str(user_id) + " User does not exist")
    db.delete(user)
    db.commit()
    

async def update_user(user_id: int, user: schema.UserCreate, db: Session):
    user_db = db.query(model.User).filter_by(id = user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail= str(user_id) + " User does not exist")
    user_db.fname = user.fname
    user_db.lname = user.lname
    user_db.email = user.email
    db.commit()
    db.refresh(user_db)
    return schema.User.from_orm(user_db)

async def get_user_logged_in(current_email: str, db: Session):
    user = db.query(model.User).filter_by(email = current_email).first()
    if user is None:
        raise HTTPException(status_code=404, detail= str(current_email) + " User does not exist")
    return schema.User.from_orm(user)

