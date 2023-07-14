import bullseye_backend.schemas.store as schema
import bullseye_backend.models.store as model

from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException


async def create_store(store: schema.Store, db: Session):
    newStore = model.Store()
    newStore.name = store.name
    newStore.state = store.state
    newStore.aisles = store.aisles
    newStore.city = store.city
    newStore.zipcode = store.zipcode
    newStore.id = store.id
    newStore.map = store.map

    db.add(newStore)
    db.commit()
    db.refresh(newStore)
    return schema.Store.from_orm(newStore)


async def get_store_by_id(store_id: int, db: Session):
    store = db.query(model.Store).filter_by(id=store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail=f"{store_id} Store does not exist")
    return schema.Store.from_orm(store)


async def get_store_by_name(store_name: str, db: Session):
    store = db.query(model.Store).filter_by(name=store_name).first()
    if store is None:
        raise HTTPException(
            status_code=404, detail=f"{store_name} Store does not exist"
        )
    return schema.Store.from_orm(store)


async def get_all_store_names(db: Session):
    store_names = db.query(model.Store).with_entities(model.Store.name).all()
    if store_names is None:
        raise HTTPException(status_code=404, detail="No stores found")
    return [name for name, in store_names]


async def delete_store(store_id: int, db: Session):
    store = db.query(model.Store).filter_by(id=store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail=f"{store_id} Store does not exist")
    db.delete(store)
    db.commit()


async def update_store(store_id: int, store: schema.Store, db: Session):
    store_db = db.query(model.Store).filter_by(id=store_id).first()
    if store_db is None:
        raise HTTPException(status_code=404, detail=f"{store_id} Store does not exist")
    store_db.name = store.name
    store_db.city = store.city
    store_db.state = store.state
    store_db.zipcode = store.zipcode
    store_db.map = store.map
    store_db.aisles = store.aisles
    db.commit()
    db.refresh(store_db)
    return schema.Store.from_orm(store_db)
