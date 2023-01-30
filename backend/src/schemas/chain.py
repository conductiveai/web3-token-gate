from pydantic import BaseModel


class Chain(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
