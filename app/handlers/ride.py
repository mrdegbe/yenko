from app.services.ride.accept import accept_ride
from app.services.ride.complete import complete_ride
from app.services.ride.create import create_ride
from app.utils.parser import parse_ride_request

from app.utils.response import error_response, success_response


def handle_ride_request(db, from_phone, text):

    pickup_location, destination = parse_ride_request(text)

    create_ride(db, from_phone, pickup_location, destination)

    return success_response("Ride request received")


from app.services.ride.accept import accept_ride


def handle_ride_acceptance(db, from_phone, text):

    parts = text.strip().split()

    if len(parts) != 2:
        return {"success": False, "message": "Invalid format"}

    _, ride_id = parts

    result = accept_ride(db, from_phone, int(ride_id))

    return result


def handle_ride_completion(db, text):

    parts = text.split()

    if len(parts) < 2:

        return error_response("Invalid format")

    ride_id = int(parts[1])

    result = complete_ride(db, ride_id)

    # if isinstance(result, dict):
    if not result["success"]:

        return error_response(result["success"])

    return success_response("Ride completed")
