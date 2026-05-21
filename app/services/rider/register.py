from app.constants.ride_status import PENDING
from app.models.rider import Rider
from app.utils.response import error_response


def register_rider(db, name, phone, location):

    existing = db.query(Rider).filter(Rider.phone == phone).first()

    if existing:

        return error_response("Rider already exists")

    rider = Rider(
        name=name, phone=phone, location=location, is_available=False, status=PENDING
    )

    db.add(rider)

    db.commit()

    db.refresh(rider)

    return rider
