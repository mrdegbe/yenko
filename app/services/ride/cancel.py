from app.models.ride import Ride
from app.constants.ride_status import CANCELLED
from app.utils.response import error_response, success_response

from app.utils.states import can_transition


def cancel_ride(db, ride_id):

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        return error_response("Ride not found")

    if not can_transition(ride.status, CANCELLED):
        return error_response(f"Cannot cancel ride from {ride.status}")

    ride.status = CANCELLED

    db.commit()

    return success_response(
        f"Ride {ride.id} cancelled", {"ride_id": ride.id, "status": ride.status}
    )
