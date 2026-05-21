from app.constants.ride_status import NO_RIDER
from app.models.rider import Rider

from app.constants.rider_status import ONLINE


def find_matching_riders(db, pickup_location):

    riders = (
        db.query(Rider)
        .filter(
            Rider.location == pickup_location,
            Rider.status == ONLINE,
            Rider.is_available == True,
        )
        .all()
    )

    if not riders:

        print(f"No riders available for {pickup_location}")

        Rider.status = NO_RIDER
        db.commit()

        return

    return riders
