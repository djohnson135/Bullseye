from pydantic import BaseModel


class Store(BaseModel):
    id: int
    name: str
    city: str
    state: str
    map: list[list[str]]
    aisles: dict
    zipcode: str

    class Config:
        orm_mode = True
