from app.utils.parser import parse_ride_request

from app.services.ride_service import create_ride, accept_ride, complete_ride
from app.utils.response import error_response, success_response


def handle_ride_request(db, from_phone, text):

    pickup, destination = parse_ride_request(text)

    create_ride(db, from_phone, pickup, destination)

    return success_response("Ride request received")


def handle_ride_acceptance(db, from_phone, text):

    parts = text.split()

    if len(parts) < 2:

        return error_response("Invalid format")

    ride_id = int(parts[1])

    result = accept_ride(db, from_phone, ride_id)

    # if isinstance(result, dict):
    if not result["success"]:

        return error_response(result["success"])

    return success_response("Ride accepted")


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
