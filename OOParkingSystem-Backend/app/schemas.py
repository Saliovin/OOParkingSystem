from datetime import datetime
from pydantic import BaseModel, conint, constr


class EntryPointMapModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class ParkingSlotMapModel(BaseModel):
    id: int
    car_id: int | None
    start_time_occupied: datetime | None

    class Config:
        orm_mode = True


class EntryPointMap(BaseModel):
    distance: int
    entry_point: EntryPointMapModel

    class Config:
        orm_mode = True


class ParkingSlotMap(BaseModel):
    distance: int
    parking_slot: ParkingSlotMapModel

    class Config:
        orm_mode = True


class EntryPointBase(BaseModel):
    pass


class EntryPointCreate(EntryPointBase):
    pass


class EntryPoint(EntryPointBase):
    id: int

    parking_slots: list[ParkingSlotMap]

    class Config:
        orm_mode = True


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


class CarBase(BaseModel):
    id: str


class CarCreate(CarBase):
    pass


class Car(CarBase):
    exit_time: datetime | None

    class Config:
        orm_mode = True


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
