from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import bullseye_backend.crud.store as crud
import bullseye_backend.schemas.store as schema

from ..dependencies import get_db

# from ..internal.map_translation.map_create import create_map

router = APIRouter(
    prefix="/store",
    tags=["store"],
    responses={404: {"description": "Not found"}},
)


@router.get("/id/{store_id}", response_model=schema.Store)
async def get_store_by_id(store_id: int, db: Session = Depends(get_db)):
    return await crud.get_store_by_id(store_id=store_id, db=db)


@router.get("/name/{store_name}", response_model=schema.Store)
async def get_store_by_name(store_name: str, db: Session = Depends(get_db)):
    store_name = store_name.replace(" ", "-").lower()
    return await crud.get_store_by_name(store_name=store_name, db=db)


@router.get("/name", response_model=List[str])
async def get_all_store_names(db: Session = Depends(get_db)):
    return await crud.get_all_store_names(db=db)


# @router.post(
#     "/gen/{store_name}/{store_state}/{store_city}/{store_id}",
#     response_model=schema.Store,
# )
# async def generate_store(
#     store_name: str,
#     store_state: str,
#     store_city: str,
#     store_id: str,
#     db: Session = Depends(get_db),
# ):
#     store_city = store_city.replace(" ", "-").lower()
#     store_name = store_name.replace(" ", "-").lower()
#     store_url = f"https://www.target.com/sl/{store_city}/{store_id}"

#     store_aisles, store_map = create_map(store_url)

#     store = schema.Store
#     store.id = store_id
#     store.name = store_name
#     store.city = store_city
#     store.state = store_state
#     store.map = store_map.tolist()
#     store.aisles = store_aisles

#     return await crud.create_store(store=store, db=db)
