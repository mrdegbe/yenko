from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session
from app.database import get_db

from app.models.ride import Ride
from app.models.rider import Rider

from app.schemas.common import ApiResponse
from typing import List

from app.auth.dependencies import get_current_admin

from app.services.rider.availability import (
    set_rider_offline,
    set_rider_offline,
    set_rider_online,
)
from app.utils.response import error_response, success_response

router = APIRouter()


@router.post("/seed-riders")
def seed_riders(db: Session = Depends(get_db)):

    existing = db.query(Rider).count()

    if existing > 0:

        return {"message": "Riders already seeded"}

    riders = [
        Rider(
            name="Kwadjo",
            phone="+233240000001",
            location="Number 4",
            status="online",
        ),
        Rider(
            name="Kwabena",
            phone="+233240000002",
            location="Nkwanta",
            status="online",
        ),
        Rider(
            name="Kwaku",
            phone="+233240000003",
            location="Anweaso",
            status="online",
        ),
        Rider(
            name="Yaw",
            phone="+233240000004",
            location="Asubone",
            status="online",
        ),
        Rider(
            name="Kofi",
            phone="+233240000005",
            location="Akwatia",
            status="online",
        ),
    ]

    db.add_all(riders)

    db.commit()

    return {"message": "Seeded"}


@router.get("/riders", response_model=ApiResponse)
def get_riders(current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):

    riders = db.query(Rider).all()

    return success_response(
        "Riders",
        [
            {
                "rider_id": rider.id,
                "name": rider.name,
                "phone": rider.phone,
                "location": rider.location,
                "status": rider.status,
                "earnings": rider.earnings,
            }
            for rider in riders
        ],
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


@router.post("/riders/{rider_id}/online")
def rider_online(
    rider_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):

    rider = set_rider_online(db, rider_id)

    if not rider:

        return {"success": False, "message": "Rider not found"}

    return {"success": True, "message": "Rider online"}


@router.post("/riders/{rider_id}/offline")
def rider_offline(
    rider_id: int,
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):

    rider = set_rider_offline(db, rider_id)

    if not rider:

        return {"success": False, "message": "Rider not found"}

    return {"success": True, "message": "Rider offline"}
