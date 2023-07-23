from datetime import datetime
from pydantic import BaseModel, constr
from app.schemas.ParkingSlotEntryPoint import EntryPointMap


class ParkingSlotBase(BaseModel):
    size: constr(pattern="['SP', 'MP', 'LP']", min_length=2, max_length=2)


class ParkingSlotCreate(ParkingSlotBase):
    pass


class ParkingSlotUpdate(BaseModel):
    id: int
    car_id: str
    start_time_occupied: datetime


class ParkingSlot(ParkingSlotBase):
    id: int
    car_id: str | None
    start_time_occupied: datetime | None

    entry_points: list[EntryPointMap]

    class Config:
        orm_mode = True
