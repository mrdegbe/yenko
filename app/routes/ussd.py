from fastapi import APIRouter, Form
from app.database import SessionLocal
from app.services.ride_service import create_ride
from app.config.locations import LOCATIONS
from app.handlers.rider_handler import handle_rider_registration
from app.services.fare_service import calculate_fare

router = APIRouter()


@router.post("/ussd")
def ussd(
    sessionId: str = Form(...),
    serviceCode: str = Form(...),
    phoneNumber: str = Form(...),
    text: str = Form(""),
):

    inputs = text.split("*")

    # MAIN MENU
    if text == "":

        return "CON Welcome to Yenko\n" "1. Request Ride\n" "2. Become Rider"

    # REQUEST RIDE
    elif inputs[0] == "1":

        # ask pickup
        if len(inputs) == 1:

            menu = "CON Select pickup location\n"

            for key, value in LOCATIONS.items():

                menu += f"{key}. {value}\n"

            return menu
            # return "CON Enter pickup location"

        # ask destination
        elif len(inputs) == 2:

            menu = "CON Select destination\n"

            for key, value in LOCATIONS.items():

                menu += f"{key}. {value}\n"

            return menu

        # create ride
        elif len(inputs) == 3:

            pickup = LOCATIONS.get(inputs[1])

            destination = LOCATIONS.get(inputs[2])

            fare = calculate_fare(pickup, destination)

            if not pickup or not destination:

                return "END Invalid location"

            db = SessionLocal()

            try:

                result = create_ride(db, phoneNumber, pickup, destination)

                # if isinstance(result, dict):
                if not result["success"]:

                    return "END No riders available right now"

            finally:

                db.close()

            return (
                f"END Ride request sent\n"
                f"{pickup} -> {destination}\n"
                f"Fare: GHS {fare}"
            )
    # BECOME RIDER
    elif inputs[0] == "2":

        db = SessionLocal()

        try:

            return handle_rider_registration(db, phoneNumber, text, LOCATIONS)

        finally:

            db.close()

    return "END Invalid choice"
