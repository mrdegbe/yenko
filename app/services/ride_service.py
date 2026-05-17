from datetime import datetime

from app.models.ride import Ride
from app.models.rider import Rider

from app.services.sms_service import send_sms
from app.services.dispatch_service import notify_riders
from app.services.rider_service import find_available_riders
from app.services.fare_service import calculate_fare
from app.utils.response import success_response, error_response


def create_ride(db, customer_phone, pickup, destination):

    fare = calculate_fare(pickup, destination)

    ride = Ride(
        customer_phone=customer_phone, pickup=pickup, destination=destination, fare=fare
    )

    db.add(ride)

    db.commit()

    db.refresh(ride)

    riders = find_available_riders(db, pickup)

    if not riders:

        ride.status = "no_rider"

        db.commit()

        return error_response("No riders available")

    notify_riders(riders, ride)

    return success_response(
        "Ride created",
        {
            "ride_id": ride.id,
            "pickup": ride.pickup,
            "destination": ride.destination,
            "fare": ride.fare,
        },
    )


def accept_ride(db, rider_phone, ride_id):

    rider = db.query(Rider).filter(Rider.phone == rider_phone).first()

    if not rider:

        return {"error": "Rider not found"}

    ride = db.query(Ride).filter(Ride.id == ride_id, Ride.status == "pending").first()

    if not ride:

        return error_response("Ride unavailable")

    if datetime.utcnow() > ride.expires_at:

        ride.status = "expired"

        db.commit()

        return {"error": "Ride expired"}

    if ride.status != "pending":

        return {"error": "Ride already taken"}

    ride.status = "accepted"

    ride.rider_id = rider.id

    ride.accepted_at = datetime.utcnow()

    rider.is_available = False

    rider.status = "busy"

    db.commit()

    send_sms(ride.customer_phone, f"{rider.name} is coming for your ride.")

    print(f"Ride {ride.id} accepted by {rider.name}")

    return success_response("Ride accepted")


def complete_ride(db, ride_id):

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:

        return error_response("Ride unavailable")

    rider = db.query(Rider).filter(Rider.id == ride.rider_id).first()

    ride.status = "completed"

    ride.completed_at = datetime.utcnow()

    if rider:

        rider.status = "available"

        rider.is_available = True

        rider.earnings += ride.fare

    db.commit()

    print(f"Ride {ride.id} completed")

    return success_response("Ride completed")
