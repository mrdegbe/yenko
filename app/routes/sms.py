from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session

from app.constants.ride_status import *
from app.database import get_db

from app.handlers.rider import go_offline, go_online
from app.models import ride
from app.models import ride
from app.models.ride import Ride
from app.models.rider import Rider

from app.schemas.common import ApiResponse
from app.schemas.ride import RideResponse
from app.schemas.rider import RiderResponse
from typing import List

from app.auth.dependencies import get_current_admin

# from app.services.expiration import expire_old_rides

from app.handlers.ride import (
    handle_ride_request,
    handle_ride_acceptance,
    handle_ride_completion,
)
from app.services.ride.complete import complete_ride as complete_ride_service


from app.services.ride.expire import expire_pending_rides
from app.services.rider.availability import (
    set_rider_offline,
    set_rider_offline,
    set_rider_online,
)
from app.utils.parser import parse_ride_request
from app.utils.response import error_response, success_response

from app.constants.ride_status import ACCEPTED, IN_PROGRESS, COMPLETED, CANCELLED

from app.services.ride.cancel import cancel_ride as cancel_ride_service

router = APIRouter()


@router.post("/sms/incoming")
def incoming_sms(
    from_phone: str = Form(...), text: str = Form(...), db: Session = Depends(get_db)
):
    expire_pending_rides(db)

    text = text.strip().upper()

    # rider accepts ride
    if text.startswith("YES"):
        return handle_ride_acceptance(db, from_phone, text)

    # complete ride
    if text.startswith("DONE"):
        return handle_ride_completion(db, text)

    if text == "ONLINE":
        return go_online(db, from_phone)

    if text == "OFFLINE":
        return go_offline(db, from_phone)

    # ride request
    if text.startswith("RIDE"):
        return handle_ride_request(db, from_phone, text)


@router.post("/rides/{ride_id}/cancel")
def cancel_ride(ride_id: int, db: Session = Depends(get_db)):

    result = cancel_ride_service(db, ride_id)

    return result
