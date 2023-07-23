from pydantic import BaseModel
from app.schemas.ParkingSlotEntryPoint import ParkingSlotMap


class EntryPointBase(BaseModel):
    pass


class EntryPointCreate(EntryPointBase):
    pass


class EntryPoint(EntryPointBase):
    id: int

    parking_slots: list[ParkingSlotMap]

    class Config:
        orm_mode = True
