# from datetime import datetime, timedelta

# from app.models.ride import Ride

# from app.constants.ride_status import PENDING, EXPIRED

# RIDE_TIMEOUT_MINUTES = 2


# def expire_old_rides(db):

#     cutoff = datetime.utcnow() - timedelta(minutes=RIDE_TIMEOUT_MINUTES)

#     rides = (
#         db.query(Ride).filter(Ride.status == PENDING, Ride.created_at < cutoff).all()
#     )

#     for ride in rides:

#         ride.status = EXPIRED

#         print(f"Ride {ride.id} expired")

#     db.commit()

from app.services.ride.expire import expire_pending_rides

__all__ = ["expire_pending_rides"]
