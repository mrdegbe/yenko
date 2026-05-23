from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.handlers.rider import go_offline, go_online
from app.handlers.ride import (
    handle_ride_request,
    handle_ride_acceptance,
    handle_ride_completion,
)

from app.services.ride.cancel import cancel_ride as cancel_ride_service
from app.services.ride.expire import expire_pending_rides

router = APIRouter()


@router.post("/sms/incoming")
def incoming_sms(
    from_: str = Form(..., alias="from"),
    text: str = Form(...),
    db: Session = Depends(get_db),
):
    expire_pending_rides(db)

    text = text.strip().upper()

    # rider accepts ride
    if text.startswith("YES"):
        return handle_ride_acceptance(db, from_, text)

    # complete ride
    if text.startswith("DONE"):
        return handle_ride_completion(db, text)

    if text == "ONLINE":
        return go_online(db, from_)

    if text == "OFFLINE":
        return go_offline(db, from_)

    # ride request
    if text.startswith("RIDE"):
        return handle_ride_request(db, from_, text)
