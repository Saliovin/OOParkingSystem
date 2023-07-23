from datetime import datetime
from pydantic import BaseModel


class CarBase(BaseModel):
    id: str


class CarCreate(CarBase):
    pass


class Car(CarBase):
    exit_time: datetime | None

    class Config:
        orm_mode = True
