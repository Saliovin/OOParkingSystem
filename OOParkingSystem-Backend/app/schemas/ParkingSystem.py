from datetime import datetime
from pydantic import BaseModel, conint, constr
from app.schemas.ParkingSlot import ParkingSlotBase


class ParkingSystemCreateParkingSlot(ParkingSlotBase):
    distances: list[int]


class ParkingSystemCreate(BaseModel):
    entry_points: conint(ge=3)
    parking_slots: list[ParkingSystemCreateParkingSlot]


class GenericSuccess(BaseModel):
    success: bool


class ParkCar(BaseModel):
    car_id: str
    car_size: constr(pattern="['S', 'M', 'L']", min_length=1, max_length=1)
    entry_point_id: int
    start_time: datetime


class UnparkCar(BaseModel):
    car_id: str
    exit_time: datetime
