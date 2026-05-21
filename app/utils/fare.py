from app.config.fares import FARES


def calculate_fare(pickup, destination):

    if pickup == destination:

        return 0

    route = tuple(sorted([pickup, destination]))

    normalized_fares = {tuple(sorted(key)): value for key, value in FARES.items()}

    return normalized_fares.get(route)
