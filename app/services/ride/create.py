from app.constants.ride_status import NO_RIDER, PENDING
from app.models.ride import Ride
from app.services.rider.match import find_matching_riders
from app.utils.fare import calculate_fare
from app.utils.response import error_response, success_response
from app.services.dispatch.broadcast import broadcast_ride_request


def create_ride(db, customer_phone, pickup_location, destination):

    fare = calculate_fare(pickup_location, destination)

    ride = Ride(
        customer_phone=customer_phone,
        pickup_location=pickup_location,
        destination=destination,
        fare=fare,
        status=PENDING,
    )

    db.add(ride)
    db.commit()
    db.refresh(ride)

    riders = find_matching_riders(db, pickup_location)

    if not riders:
        ride.status = NO_RIDER
        db.commit()

        return error_response("No riders available")

    broadcast_ride_request(riders, ride)

    return ride
