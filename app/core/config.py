from dotenv import load_dotenv

import os

load_dotenv()


class Settings:

    APP_NAME = os.getenv("APP_NAME")

    ENVIRONMENT = os.getenv("ENVIRONMENT")

    DATABASE_URL = os.getenv("DATABASE_URL")

    AFRICASTALKING_USERNAME = os.getenv("AFRICASTALKING_USERNAME")

    AFRICASTALKING_API_KEY = os.getenv("AFRICASTALKING_API_KEY")

    DISPATCH_TIMEOUT = int(os.getenv("DISPATCH_TIMEOUT", 120))


settings = Settings()
