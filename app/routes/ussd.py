from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from app.database import SessionLocal
from app.services.ride.create import create_ride
from app.config.locations import LOCATIONS
from app.handlers.rider import handle_rider_registration
from app.utils.fare import calculate_fare

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

        return PlainTextResponse(
            "CON Welcome to Yenko\n" "1. Request Ride\n" "2. Become Rider"
        )

    # REQUEST RIDE
    elif inputs[0] == "1":

        # ask pickup location
        if len(inputs) == 1:

            menu = "CON Select pickup location\n"

            for key, value in LOCATIONS.items():

                menu += f"{key}. {value}\n"

            return PlainTextResponse(menu)

        # ask destination
        elif len(inputs) == 2:

            menu = "CON Select destination\n"

            for key, value in LOCATIONS.items():

                menu += f"{key}. {value}\n"

            return PlainTextResponse(menu)

        # create ride
        elif len(inputs) == 3:

            pickup_location = LOCATIONS.get(inputs[1])

            destination = LOCATIONS.get(inputs[2])

            if not pickup_location or not destination:

                return PlainTextResponse("END Invalid location")

            db = SessionLocal()

            try:

                result = create_ride(db, phoneNumber, pickup_location, destination)

                # if not result:
                if not result["success"]:

                    return PlainTextResponse(f"END {result['message']}")

                ride = result["data"]

            finally:

                db.close()

            return PlainTextResponse(
                f"END Ride request sent\n"
                f"{ride.pickup_location} -> {ride.destination}\n"
                f"Fare: GHS {ride.fare}"
            )
    # BECOME RIDER
    elif inputs[0] == "2":

        db = SessionLocal()

        try:

            return handle_rider_registration(db, phoneNumber, text, LOCATIONS)

        finally:

            db.close()

    return PlainTextResponse("END Invalid choice")
