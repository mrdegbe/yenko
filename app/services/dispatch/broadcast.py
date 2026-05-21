from app.services.sms_service import send_sms


def broadcast_ride_request(riders, ride):

    if not riders:

        print(f"No riders available for {ride.pickup_location}")

        return

    for rider in riders:

        message = (
            f"YENKO RIDE\n"
            f"{ride.pickup_location} -> {ride.destination}\n"
            f"Fare: GHS {ride.fare}\n"
            f"Reply YES {ride.id}"
        )

        send_sms(rider.phone, message)
