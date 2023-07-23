from datetime import datetime
import math

parking_slot_pricing = {"SP": 20, "MP": 60, "LP": 100, "full": 5000, "starting": 40}


def get_parking_fee(
    start_date: datetime,
    end_date: datetime,
    parking_slot_size: int,
    prev_exit_date: datetime = None,
):
    delta = end_date - start_date
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
