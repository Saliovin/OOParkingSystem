from datetime import datetime
from pydantic import BaseModel


class ParkingSlotEntryPointBase(BaseModel):
    slot_id: int
    entry_id: int
    distance: int


class ParkingSlotEntryPointCreate(ParkingSlotEntryPointBase):
    pass


class ParkingSlotEntryPoint(ParkingSlotEntryPointBase):
    id: int

    class Config:
        orm_mode = True


class ParkingSlotMapModel(BaseModel):
    id: int
    car_id: int | None
    start_time_occupied: datetime | None

    class Config:
        orm_mode = True


class ParkingSlotMap(BaseModel):
    distance: int
    parking_slot: ParkingSlotMapModel

    class Config:
        orm_mode = True


class EntryPointMapModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class EntryPointMap(BaseModel):
    distance: int
    entry_point: EntryPointMapModel

    class Config:
        orm_mode = True
