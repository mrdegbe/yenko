from app.core.config import settings

username = settings.AFRICASTALKING_USERNAME

api_key = settings.AFRICASTALKING_API_KEY


def send_sms(phone, message):

    print("\n========== YENKO SMS ==========")

    print(f"TO: {phone}")

    print(message)

    print("================================\n")
