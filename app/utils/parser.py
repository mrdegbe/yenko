def parse_ride_request(text):

    _, payload = text.split(" ", 1)

    pickup, destination = payload.split("|")

    return pickup.strip(), destination.strip()
