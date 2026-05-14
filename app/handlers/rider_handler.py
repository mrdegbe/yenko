from app.models.rider import Rider


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
