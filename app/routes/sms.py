from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.ride import Ride
from app.models.rider import Rider

from app.handlers.ride_handler import (
    handle_ride_request,
    handle_ride_acceptance,
    handle_ride_completion,
)

from app.handlers.rider_handler import go_online, go_offline


from app.utils.parser import parse_ride_request

router = APIRouter()


@router.post("/sms/incoming")
def incoming_sms(
    from_phone: str = Form(...), text: str = Form(...), db: Session = Depends(get_db)
):

    text = text.strip().upper()

    # rider accepts ride
    if text.startswith("YES"):
        return handle_ride_acceptance(db, from_phone, text)

        # parts = text.split()
        # if len(parts) < 2:
        #     return {"message": "Invalid format"}
        # ride_id = int(parts[1])
        # result = accept_ride(db, from_phone, ride_id)
        # if isinstance(result, dict):
        #     return result
        # return {"message": "Ride accepted"}

    # complete ride
    if text.startswith("DONE"):
        return handle_ride_completion(db, text)

        # parts = text.split()
        # if len(parts) < 2:
        #     return {"message": "Invalid format"}
        # ride_id = int(parts[1])
        # result = complete_ride(db, ride_id)
        # if isinstance(result, dict):
        #     return result
        # return {"message": "Ride completed"}

    if text == "ONLINE":
        return go_online(db, from_phone)

        # rider = db.query(Rider).filter(Rider.phone == from_phone).first()
        # if not rider:
        #     return {"message": "Rider not found"}
        # rider.status = "available"
        # rider.is_available = True
        # db.commit()
        # return {"message": "You are now online"}

    if text == "OFFLINE":
        return go_offline(db, from_phone)

        # rider = db.query(Rider).filter(Rider.phone == from_phone).first()
        # if not rider:
        #     return {"message": "Rider not found"}
        # rider.status = "offline"
        # rider.is_available = False
        # db.commit()
        # return {"message": "You are now offline"}

    # ride request
    if text.startswith("RIDE"):
        return handle_ride_request(db, from_phone, text)

        # pickup, destination = parse_ride_request(text)
        # create_ride(db, from_phone, pickup, destination)
        # return {"message": "Ride created"}


@router.post("/seed-riders")
def seed_riders(db: Session = Depends(get_db)):

    existing = db.query(Rider).count()

    if existing > 0:

        return {"message": "Riders already seeded"}

    riders = [
        Rider(
            name="Kwame", phone="+233540000001", location="Anweaso", status="available"
        ),
        Rider(
            name="Yaw", phone="+233540000002", location="Akwatia", status="available"
        ),
    ]

    db.add_all(riders)

    db.commit()

    return {"message": "Seeded"}


@router.get("/rides")
def get_rides(db: Session = Depends(get_db)):

    rides = db.query(Ride).all()

    return rides


@router.get("/riders")
def get_riders(db: Session = Depends(get_db)):

    riders = db.query(Rider).all()

    return riders


@router.get("/active-rides")
def active_rides(db: Session = Depends(get_db)):

    rides = db.query(Ride).filter(Ride.status.in_(["pending", "accepted"])).all()

    return rides
