from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas.Car import Car, CarCreate
from app.schemas.Entrypoint import EntryPoint
from app.schemas.ParkingSlot import ParkingSlot, ParkingSlotCreate
from app.schemas.ParkingSlotEntryPoint import (
    ParkingSlotEntryPoint,
    ParkingSlotEntryPointCreate,
)
from app.schemas.ParkingSystem import (
    GenericSuccess,
    ParkCar,
    ParkingSystemCreate,
    UnparkCar,
)
from app.database.database import get_db
from app.utils import get_parking_fee
from . import api


app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/entry-points", response_model=EntryPoint)
def create_entry_point(db: Session = Depends(get_db)):
    return api.create_entry_point(db=db)


@app.get("/entry-points", response_model=list[EntryPoint])
def read_entry_points(db: Session = Depends(get_db)):
    entry_points = api.get_entry_point_collection(db)
    return entry_points


@app.get("/entry-points/{entry_point_id}", response_model=EntryPoint)
def read_entry_point(entry_point_id: int, db: Session = Depends(get_db)):
    db_entry_point = api.get_entry_point(db, entry_point_id=entry_point_id)
    if db_entry_point is None:
        raise HTTPException(status_code=404, detail="Entry point not found")
    return db_entry_point


@app.post("/parking-slots", response_model=ParkingSlot)
def create_parking_slot(parking_slot: ParkingSlotCreate, db: Session = Depends(get_db)):
    return api.create_parking_slot(db=db, parking_slot=parking_slot)


@app.get("/parking-slots", response_model=list[ParkingSlot])
def read_parking_slots(db: Session = Depends(get_db)):
    parking_slots = api.get_parking_slot_collection(db)
    return parking_slots


@app.get("/parking-slots/{parking_slot_id}", response_model=ParkingSlot)
def read_parking_slot(parking_slot_id: int, db: Session = Depends(get_db)):
    db_parking_slot = api.get_parking_slot(db, parking_slot_id=parking_slot_id)
    if db_parking_slot is None:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return db_parking_slot


@app.post("/slot-entry", response_model=ParkingSlotEntryPoint)
def create_parking_slot_entry_point(
    parking_slot_entry_point: ParkingSlotEntryPointCreate,
    db: Session = Depends(get_db),
):
    return api.create_parking_slot_entry_point(
        db=db, parking_slot_entry_point=parking_slot_entry_point
    )


@app.get("/slot-entry", response_model=list[ParkingSlotEntryPoint])
def read_parking_slot_entry_points(db: Session = Depends(get_db)):
    parking_slot_entry_points = api.get_parking_slot_entry_point_collection(db)
    return parking_slot_entry_points


@app.get(
    "/slot-entry/{parking_slot_entry_point_id}",
    response_model=ParkingSlotEntryPoint,
)
def read_parking_slot_entry_point(
    parking_slot_entry_point_id: int, db: Session = Depends(get_db)
):
    db_parking_slot_entry_point = api.get_parking_slot_entry_point(
        db, parking_slot_entry_point_id=parking_slot_entry_point_id
    )
    if db_parking_slot_entry_point is None:
        raise HTTPException(
            status_code=404, detail="Parking slot entry point relationship not found"
        )
    return db_parking_slot_entry_point


@app.post("/cars", response_model=Car)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    return api.create_car(db=db, car_id=car.id)


@app.get("/cars", response_model=list[Car])
def read_cars(db: Session = Depends(get_db)):
    cars = api.get_car_collection(db)
    return cars


@app.get("/cars/{car_id}", response_model=Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = api.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.post("/new-parking-system", response_model=GenericSuccess)
def create_new_parking_system(
    parking_system: ParkingSystemCreate, db: Session = Depends(get_db)
):
    return api.start_new_parking_system(db=db, parking_system=parking_system)


@app.post("/park-car")
def park_car(park_car: ParkCar, db: Session = Depends(get_db)):
    parking_slot = api.get_available_parking_slot(db=db, park_car=park_car)
    if parking_slot is None:
        raise HTTPException(status_code=404, detail="No available parking slot found")
    db_car = api.get_car(db, car_id=park_car.car_id)
    if db_car is None:
        db_car = api.create_car(db=db, car_id=park_car.car_id)
    return api.update_parking_slot(
        db=db,
        parking_slot=parking_slot,
        car_id=db_car.id,
        start_time=park_car.start_time,
    )


@app.post("/unpark-car")
def unpark_car(unpark_car: UnparkCar, db: Session = Depends(get_db)):
    parking_slot = api.get_parking_slot_by_car_id(db=db, car_id=unpark_car.car_id)
    if parking_slot is None:
        raise HTTPException(status_code=404, detail="No parking slot with car id found")
    db_car = api.get_car(db, car_id=unpark_car.car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="No car found")
    prev_exit_date = db_car.exit_time
    start_time_occupied = parking_slot.start_time_occupied
    api.update_parking_slot(
        db=db, parking_slot=parking_slot, car_id=None, start_time=None
    )
    db_car = api.update_car(db=db, car=db_car, exit_time=unpark_car.exit_time)
    return get_parking_fee(
        start_date=start_time_occupied,
        end_date=db_car.exit_time,
        parking_slot_size=parking_slot.size,
        prev_exit_date=prev_exit_date,
    )
