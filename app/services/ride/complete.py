from app.models.ride import Ride
from app.constants.ride_status import ACCEPTED, COMPLETED


def complete_ride(db, ride_id):

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:

        return {"success": False, "message": "Ride not found"}

    if ride.status != ACCEPTED:

        return {"success": False, "message": "Only accepted rides can be completed"}

    rider = ride.rider

    ride.status = COMPLETED

    if rider:

        rider.earnings += ride.fare or 0

        rider.is_available = True

    db.commit()

    return {"success": True, "message": "Ride completed", "ride": ride, "rider": rider}
