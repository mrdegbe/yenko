from datetime import datetime, timedelta

from app.constants.ride_status import EXPIRED
from app.models.ride import Ride


def expire_pending_rides(db, timeout_minutes=2):

    cutoff = datetime.utcnow() - timedelta(minutes=timeout_minutes)

    rides = (
        db.query(Ride).filter(Ride.status == "pending", Ride.created_at < cutoff).all()
    )

    expired_count = 0

    for ride in rides:

        ride.status = EXPIRED

        expired_count += 1

        print(f"Ride {ride.id} expired")

    db.commit()

    return {"success": True, "expired_count": expired_count}
