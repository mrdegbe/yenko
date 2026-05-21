from fastapi import APIRouter, Depends
from requests import Session

from app.auth.dependencies import get_current_admin
from app.constants.ride_status import ACCEPTED, CANCELLED, IN_PROGRESS, PENDING
from app.database import get_db
from app.models.ride import Ride
from app.schemas.common import ApiResponse
from app.utils.response import success_response
from app.services.ride.complete import complete_ride as crs

router = APIRouter()


@router.get("/rides", response_model=ApiResponse)
def get_rides(current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):

    rides = db.query(Ride).all()

    return success_response(
        "Rides fetched",
        [
            {
                "ride_id": ride.id,
                "pickup": ride.pickup_location,
                "destination": ride.destination,
                "fare": ride.fare,
                "status": ride.status,
            }
            for ride in rides
        ],
    )


@router.get("/active-rides")
def active_rides(db: Session = Depends(get_db)):

    rides = db.query(Ride).filter(Ride.status.in_([PENDING, ACCEPTED])).all()

    return (
        success_response(
            "Active rides",
            [
                {
                    "ride_id": ride.id,
                    "pickup": ride.pickup_location,
                    "destination": ride.destination,
                    "fare": ride.fare,
                    "status": ride.status,
                }
                for ride in rides
            ],
        ),
    )


@router.post("/rides/{ride_id}/start")
def start_ride(
    ride_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:

        return {"success": False, "message": "Ride not found"}

    if ride.status != ACCEPTED:

        return {"success": False, "message": "Ride not accepted"}

    ride.status = IN_PROGRESS

    db.commit()

    return {"success": True, "message": "Ride started"}


@router.post("/rides/{ride_id}/complete")
def complete_ride(
    ride_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):

    result = crs(db, ride_id)

    return result


@router.post("/rides/{ride_id}/cancel")
def cancel_ride(
    ride_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:

        return {"success": False, "message": "Ride not found"}

    ride.status = CANCELLED

    rider = ride.rider

    if rider:

        rider.is_available = True

    db.commit()

    return {"success": True, "message": "Ride cancelled"}
