from pydantic import BaseModel, Field


class UserBase(BaseModel):
    # metadata: dict[str, str] = Field(alias='metadata_')
    fname: str
    lname: str


class User(UserBase):
    id: int
    email: str
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    fname: str
    lname: str
    email: str
    class Config:
        orm_mode = True
    # metadata_ = sa.Column('metadata', sa.JSON)
