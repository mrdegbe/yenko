from app.models.rider import Rider
from app.services.rider_service import register_rider


def go_online(db, from_phone):

    rider = db.query(Rider).filter(Rider.phone == from_phone).first()

    if not rider:

        return {"message": "Rider not found"}

    rider.status = "available"

    rider.is_available = True

    db.commit()

    return {"message": "You are now online"}


def go_offline(db, from_phone):

    rider = db.query(Rider).filter(Rider.phone == from_phone).first()

    if not rider:

        return {"message": "Rider not found"}

    rider.status = "offline"

    rider.is_available = False

    db.commit()

    return {"message": "You are now offline"}


def handle_rider_registration(db, phone, text, locations):

    inputs = text.split("*")

    if len(inputs) == 1:

        return "CON Enter your name"

    elif len(inputs) == 2:

        menu = "CON Select your area\n"

        for key, value in locations.items():

            menu += f"{key}. {value}\n"

        return menu

    elif len(inputs) == 3:

        name = inputs[1]

        location = locations.get(inputs[2])

        if not location:

            return "END Invalid location"

        result = register_rider(db, name, phone, location)

        if isinstance(result, dict):

            return "END Rider already exists"

        return f"END Welcome to Yenko Rider\n" f"{name} registered successfully"
