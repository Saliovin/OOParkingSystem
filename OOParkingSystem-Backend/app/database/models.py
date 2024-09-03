from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class ParkingSlotEntryPoint(Base):
    __tablename__ = "parking_slot_entry_point"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("parking_slot.id"), index=True)
    entry_id = Column(Integer, ForeignKey("entry_point.id"), index=True)
    distance = Column(Integer, index=True)

    parking_slot = relationship(
        "ParkingSlot", lazy="joined", back_populates="entry_points"
    )
    entry_point = relationship(
        "EntryPoint", lazy="joined", back_populates="parking_slots"
    )


class EntryPoint(Base):
    __tablename__ = "entry_point"

    id = Column(Integer, primary_key=True, index=True)

    parking_slots = relationship(
        "ParkingSlotEntryPoint",
        back_populates="entry_point",
    )


class ParkingSlot(Base):
    __tablename__ = "parking_slot"

    id = Column(Integer, primary_key=True, index=True)
    size = Column(String(2), index=True)
    car_id = Column(String, ForeignKey("car.id"), index=True)
    start_time_occupied = Column(DateTime)

    entry_points = relationship(
        "ParkingSlotEntryPoint",
        back_populates="parking_slot",
    )


class Car(Base):
    __tablename__ = "car"

    id = Column(String, primary_key=True, index=True)
    exit_time = Column(DateTime)
