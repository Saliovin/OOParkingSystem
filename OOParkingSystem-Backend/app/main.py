from datetime import datetime
import math
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import api, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

parking_slot_pricing = {"SP": 20, "MP": 60, "LP": 100, "full": 5000, "starting": 40}


def get_parking_fee(
    start_date: datetime,
    end_date: datetime,
    parking_slot_size: int,
    prev_exit_date: datetime = None,
):
    delta = start_date - end_date
    hours_parked = math.ceil(delta.total_seconds() / 3600)
    days_parked = math.floor(hours_parked / 24)
    hours_parked_remainder = hours_parked - (days_parked * 24)
    parking_fee = 0
    if days_parked:
        parking_fee += days_parked * parking_slot_pricing["full"]
        parking_fee += hours_parked_remainder * parking_slot_pricing[parking_slot_size]
    else:
        if hours_parked_remainder > 3:
            parking_fee += (hours_parked_remainder - 3) * parking_slot_pricing[
                parking_slot_size
            ]
            hours_parked_remainder = 3
        continuous_fee = parking_slot_pricing["starting"]
        if prev_exit_date:
            delta_last_park = start_date - prev_exit_date
            hours_last_park = delta_last_park.total_seconds() / 3600
            if hours_last_park < 1:
                continuous_fee = parking_slot_pricing[parking_slot_size]
        parking_fee += hours_parked_remainder * continuous_fee

    return parking_fee


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/entry-points", response_model=schemas.EntryPoint)
def create_entry_point(db: Session = Depends(get_db)):
    return api.create_entry_point(db=db)


@app.get("/entry-points", response_model=list[schemas.EntryPoint])
def read_entry_points(db: Session = Depends(get_db)):
    entry_points = api.get_entry_point_collection(db)
    print(entry_points[0].parking_slots[0].parking_slot.size)
    return entry_points


@app.get("/entry-points/{entry_point_id}", response_model=schemas.EntryPoint)
def read_entry_point(entry_point_id: int, db: Session = Depends(get_db)):
    db_entry_point = api.get_entry_point(db, entry_point_id=entry_point_id)
    if db_entry_point is None:
        raise HTTPException(status_code=404, detail="Entry point not found")
    return db_entry_point


@app.post("/parking-slots", response_model=schemas.ParkingSlot)
def create_parking_slot(
    parking_slot: schemas.ParkingSlotCreate, db: Session = Depends(get_db)
):
    return api.create_parking_slot(db=db, parking_slot=parking_slot)


@app.get("/parking-slots", response_model=list[schemas.ParkingSlot])
def read_parking_slots(db: Session = Depends(get_db)):
    parking_slots = api.get_parking_slot_collection(db)
    return parking_slots


@app.get("/parking-slots/{parking_slot_id}", response_model=schemas.ParkingSlot)
def read_parking_slot(parking_slot_id: int, db: Session = Depends(get_db)):
    db_parking_slot = api.get_parking_slot(db, parking_slot_id=parking_slot_id)
    if db_parking_slot is None:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return db_parking_slot


@app.post("/slot-entry", response_model=schemas.ParkingSlotEntryPoint)
def create_parking_slot_entry_point(
    parking_slot_entry_point: schemas.ParkingSlotEntryPointCreate,
    db: Session = Depends(get_db),
):
    return api.create_parking_slot_entry_point(
        db=db, parking_slot_entry_point=parking_slot_entry_point
    )


@app.get("/slot-entry", response_model=list[schemas.ParkingSlotEntryPoint])
def read_parking_slot_entry_points(db: Session = Depends(get_db)):
    parking_slot_entry_points = api.get_parking_slot_entry_point_collection(db)
    return parking_slot_entry_points


@app.get(
    "/slot-entry/{parking_slot_entry_point_id}",
    response_model=schemas.ParkingSlotEntryPoint,
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


@app.post("/cars", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return api.create_car(db=db, car=car)


@app.get("/cars", response_model=list[schemas.Car])
def read_cars(db: Session = Depends(get_db)):
    cars = api.get_car_collection(db)
    return cars


@app.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = api.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.post("/new-parking-system", response_model=schemas.GenericSuccess)
def create_new_parking_system(
    parking_system: schemas.ParkingSystemCreate, db: Session = Depends(get_db)
):
    return api.start_new_parking_system(db=db, parking_system=parking_system)


@app.post("/park-car")
def park_car(park_car: schemas.ParkCar, db: Session = Depends(get_db)):
    parking_slot = api.get_available_parking_slot(db=db, park_car=park_car)
    if parking_slot is None:
        raise HTTPException(status_code=404, detail="No available parking slot found")
    db_car = api.get_car(db, car_id=park_car.car_id)
    if db_car is None:
        db_car = api.create_car(db=db, car={"id": park_car.car_id})
    return api.update_parking_slot(
        db=db, parking_slot=parking_slot, car=db_car, start_time=park_car.start_time
    )


@app.post("/unpark-car")
def upark_car(unpark_car: schemas.UnparkCar, db: Session = Depends(get_db)):
    parking_slot = api.get_parking_slot_by_car_id(db=db, car_id=unpark_car.car_id)
    if parking_slot is None:
        raise HTTPException(status_code=404, detail="No parking slot with car id found")
    db_car = api.get_car(db, car_id=park_car.car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="No car found")
    prev_exit_date = db_car.exit_time
    api.update_parking_slot(db=db, parking_slot=parking_slot, car=db_car)
    db_car = api.update_car(db=db, car=db_car, exit_time=unpark_car.exit_time)
    return get_parking_fee(
        start_date=parking_slot.start_time_occupied,
        end_date=db_car.exit_time,
        prev_exit_date=prev_exit_date,
    )
