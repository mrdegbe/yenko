from app.models.rider import Rider


def find_available_riders(db, pickup):

    riders = (
        db.query(Rider)
        .filter(Rider.location == pickup, Rider.is_available == True)
        .all()
    )

    return riders
