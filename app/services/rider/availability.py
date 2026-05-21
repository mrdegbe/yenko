from app.constants.rider_status import BUSY, OFFLINE, ONLINE
from app.models.rider import Rider


def set_rider_online(db, rider_id):

    rider = db.query(Rider).filter(Rider.id == rider_id).first()

    if not rider:

        return None

    rider.status = ONLINE

    rider.is_available = True

    db.commit()

    return rider


def set_rider_offline(db, rider_id):

    rider = db.query(Rider).filter(Rider.id == rider_id).first()

    if not rider:

        return None

    rider.status = OFFLINE

    rider.is_available = False

    db.commit()

    return rider


def set_rider_busy(db, rider_id):

    rider = db.query(Rider).filter(Rider.id == rider_id).first()

    if not rider:

        return None

    rider.status = BUSY

    rider.is_available = False

    db.commit()

    return rider
