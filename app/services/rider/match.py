from app.models.rider import Rider
from app.constants.rider_status import ONLINE


def find_matching_riders(db, pickup_location):

    print("Searching pickup:", pickup_location)

    riders = (
        db.query(Rider)
        .filter(
            Rider.location == pickup_location,
            Rider.status == ONLINE,
            Rider.is_available == True,
        )
        .all()
    )

    print("Matched riders:", len(riders))

    for rider in riders:

        print(rider.name, rider.location, rider.status, rider.is_available)

    return riders
