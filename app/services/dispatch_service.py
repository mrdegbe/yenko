from app.services.sms_service import send_sms


def notify_riders(riders, ride):

    for rider in riders:

        message = (
            f"YENKO RIDE\n"
            f"{ride.pickup} -> {ride.destination}\n"
            f"Reply YES {ride.id}"
        )

        send_sms(rider.phone, message)
