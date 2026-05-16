from app.utils.parser import parse_ride_request

from app.services.ride_service import create_ride, accept_ride, complete_ride


def handle_ride_request(db, from_phone, text):

    pickup, destination = parse_ride_request(text)

    create_ride(db, from_phone, pickup, destination)

    return {"message": "Ride created"}


def handle_ride_acceptance(db, from_phone, text):

    parts = text.split()

    if len(parts) < 2:

        return {"message": "Invalid format"}

    ride_id = int(parts[1])

    result = accept_ride(db, from_phone, ride_id)

    if isinstance(result, dict):

        return {"message": result["error"]}

    return {"message": "Ride accepted"}


def handle_ride_completion(db, text):

    parts = text.split()

    if len(parts) < 2:

        return {"message": "Invalid format"}

    ride_id = int(parts[1])

    result = complete_ride(db, ride_id)

    if isinstance(result, dict):

        return {"message": result["error"]}

    return {"message": "Ride completed"}
