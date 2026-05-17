from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import ride
from app.models import ride
from app.models.ride import Ride
from app.models.rider import Rider

from app.schemas.common import ApiResponse
from app.schemas.ride import RideResponse
from app.schemas.rider import RiderResponse
from typing import List

from app.auth.dependencies import get_current_admin

from app.handlers.ride_handler import (
    handle_ride_request,
    handle_ride_acceptance,
    handle_ride_completion,
)

from app.handlers.rider_handler import go_online, go_offline


from app.utils.parser import parse_ride_request
from app.utils.response import error_response, success_response

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
            name="Kwame", phone="+233240000001", location="Anweaso", status="available"
        ),
        Rider(
            name="Yaw", phone="+233240000002", location="Anweaso", status="available"
        ),
    ]

    db.add_all(riders)

    db.commit()

    return {"message": "Seeded"}


@router.get("/rides", response_model=ApiResponse)
def get_rides(current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):

    rides = db.query(Ride).all()

    return success_response(
        "Rides fetched",
        [
            {
                "ride_id": ride.id,
                "pickup": ride.pickup,
                "destination": ride.destination,
                "fare": ride.fare,
                "status": ride.status,
            }
            for ride in rides
        ],
    )


@router.get("/riders", response_model=ApiResponse)
def get_riders(current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):

    riders = db.query(Rider).all()

    return success_response(
        "Riders",
        [
            {"name": rider.name, "phone": rider.phone, "location": rider.location}
            for rider in riders
        ],
    )


@router.get("/active-rides")
def active_rides(db: Session = Depends(get_db)):

    rides = db.query(Ride).filter(Ride.status.in_(["pending", "accepted"])).all()

    return (
        success_response(
            "Active rides",
            [
                {
                    "ride_id": ride.id,
                    "pickup": ride.pickup,
                    "destination": ride.destination,
                    "fare": ride.fare,
                    "status": ride.status,
                }
                for ride in rides
            ],
        ),
    )


@router.post("/approve-rider/{rider_id}")
def approve_rider(rider_id: int, db: Session = Depends(get_db)):

    rider = db.query(Rider).filter(Rider.id == rider_id).first()

    if not rider:

        return error_response("Rider not found")

    rider.status = "available"

    rider.is_available = True

    db.commit()

    return success_response("Rider approved and is now online")


@router.get("/rider-summary/{rider_id}")
def rider_summary(rider_id: int, db: Session = Depends(get_db)):

    rider = db.query(Rider).filter(Rider.id == rider_id).first()

    if not rider:

        return error_response("Rider not found")

    rides = db.query(Ride).filter(Ride.rider_id == rider.id).all()

    return success_response(
        "Rider summary",
        {
            "rider": rider.name,
            "location": rider.location,
            "status": rider.status,
            "earnings": rider.earnings,
            "total_rides": len(rides),
        },
    )
