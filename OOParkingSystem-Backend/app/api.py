from datetime import datetime
from sqlalchemy.orm import Session

from app.database import clear_data

from . import models, schemas

car_size_slot_size_mapping = {
    "S": ["SP", "MP", "LP"],
    "M": ["MP", "LP"],
    "L": ["LP"],
}


def get_entry_point(db: Session, entry_point_id: int):
    return (
        db.query(models.EntryPoint)
        .filter(models.EntryPoint.id == entry_point_id)
        .first()
    )


def get_entry_point_collection(db: Session):
    return db.query(models.EntryPoint).all()


def create_entry_point(db: Session):
    db_entry_point = models.EntryPoint()
    db.add(db_entry_point)
    db.commit()
    db.refresh(db_entry_point)
    return db_entry_point


def get_parking_slot(db: Session, parking_slot_id: int):
    return (
        db.query(models.ParkingSlot)
        .filter(models.ParkingSlot.id == parking_slot_id)
        .first()
    )


def get_parking_slot_by_car_id(db: Session, car_id: int):
    return (
        db.query(models.ParkingSlot).filter(models.ParkingSlot.car_id == car_id).first()
    )


def get_parking_slot_collection(db: Session):
    return db.query(models.ParkingSlot).all()


def create_parking_slot(db: Session, parking_slot: schemas.ParkingSlotCreate):
    db_parking_slot = models.ParkingSlot(size=parking_slot.size)
    db.add(db_parking_slot)
    db.commit()
    db.refresh(db_parking_slot)
    return db_parking_slot


def update_parking_slot(
    db: Session,
    parking_slot: schemas.ParkingSlot,
    car_id: str,
    start_time: datetime,
):
    parking_slot.car_id = car_id
    parking_slot.start_time_occupied = start_time
    db.commit()
    db.refresh(parking_slot)
    return parking_slot


def update_car(db: Session, car: schemas.Car, exit_time: datetime):
    car.exit_time = exit_time
    db.commit()
    db.refresh(car)
    return car


def get_parking_slot_entry_point(db: Session, parking_slot_entry_point_id: int):
    return (
        db.query(models.ParkingSlotEntryPoint)
        .filter(models.ParkingSlotEntryPoint.id == parking_slot_entry_point_id)
        .first()
    )


def get_parking_slot_entry_point_collection(db: Session):
    return db.query(models.ParkingSlotEntryPoint).all()


def create_parking_slot_entry_point(
    db: Session, parking_slot_entry_point: schemas.ParkingSlotEntryPointCreate
):
    db_parking_slot_entry_point = models.ParkingSlotEntryPoint(
        slot_id=parking_slot_entry_point.slot_id,
        entry_id=parking_slot_entry_point.entry_id,
        distance=parking_slot_entry_point.distance,
    )
    db.add(db_parking_slot_entry_point)
    db.commit()
    db.refresh(db_parking_slot_entry_point)
    return db_parking_slot_entry_point


def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def get_car_collection(db: Session):
    return db.query(models.Car).all()


def create_car(db: Session, car_id: str):
    db_car = models.Car(id=car_id)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def start_new_parking_system(db: Session, parking_system: schemas.ParkingSystemCreate):
    clear_data(db)
    db_entry_point_list = []
    for i in range(parking_system.entry_points):
        db_entry_point = models.EntryPoint()
        db.add(db_entry_point)
        db_entry_point_list.append(db_entry_point)
    for parking_slot in parking_system.parking_slots:
        db_parking_slot = models.ParkingSlot(size=parking_slot.size)
        db.add(db_parking_slot)
        for i, distance in enumerate(parking_slot.distances):
            db_parking_slot_entry_point = models.ParkingSlotEntryPoint(
                distance=distance,
            )
            db_parking_slot_entry_point.parking_slot = db_parking_slot
            db_entry_point_list[i].parking_slots.append(db_parking_slot_entry_point)

            db.add(db_parking_slot_entry_point)
    db.commit()
    return {"success": True}


def get_available_parking_slot(db: Session, park_car: schemas.ParkCar):
    parking_slot_entry_point = (
        db.query(models.ParkingSlotEntryPoint)
        .filter(models.ParkingSlotEntryPoint.entry_id == park_car.entry_point_id)
        .filter(
            models.ParkingSlotEntryPoint.parking_slot.has(
                models.ParkingSlot.car_id == None
            )
        )
        .filter(
            models.ParkingSlotEntryPoint.parking_slot.has(
                models.ParkingSlot.size.in_(
                    car_size_slot_size_mapping[park_car.car_size]
                )
            )
        )
        .order_by(models.ParkingSlotEntryPoint.distance)
    ).first()
    if parking_slot_entry_point is None:
        return None
    return parking_slot_entry_point.parking_slot


def unpark_car(db: Session):
    pass
