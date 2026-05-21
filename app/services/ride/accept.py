from datetime import datetime

from app.constants.ride_status import EXPIRED, PENDING, ACCEPTED

from app.constants.rider_status import BUSY

from app.models.ride import Ride
from app.models.rider import Rider

from app.services.rider.availability import set_rider_busy
from app.services.sms_service import send_sms

from app.utils.response import error_response, success_response

from app.utils.states import can_transition


def accept_ride(db, rider_phone, ride_id):

    rider = db.query(Rider).filter(Rider.phone == rider_phone).first()

    if not rider:
        return error_response("Rider not found")

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        return error_response("Ride unavailable")

    if datetime.utcnow() > ride.expires_at:

        if can_transition(ride.status, EXPIRED):
            ride.status = EXPIRED
            db.commit()

        return error_response("Ride request expired")

    if not can_transition(ride.status, ACCEPTED):
        return error_response(f"Cannot accept ride from {ride.status}")

    ride.status = ACCEPTED

    ride.rider_id = rider.id

    ride.accepted_at = datetime.utcnow()

    set_rider_busy(db, rider.id)

    rider.status = BUSY

    db.commit()

    send_sms(ride.customer_phone, f"{rider.name} is coming for your ride.")

    print(f"Ride {ride.id} accepted by {rider.name}")

    return success_response("Ride accepted", {"ride_id": ride.id, "rider": rider.name})
