from app.models.rider import Rider


def find_available_riders(db, pickup):

    riders = (
        db.query(Rider)
        .filter(Rider.location == pickup, Rider.is_available == True)
        .all()
    )

    return riders


def register_rider(db, name, phone, location):

    existing = db.query(Rider).filter(Rider.phone == phone).first()

    if existing:

        return {"error": "Rider already exists"}

    rider = Rider(
        name=name, phone=phone, location=location, is_available=False, status="pending"
    )

    db.add(rider)

    db.commit()

    db.refresh(rider)

    return rider
