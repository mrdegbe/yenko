from app.constants.ride_states import ALLOWED_TRANSITIONS


def can_transition(current_status, new_status):

    allowed = ALLOWED_TRANSITIONS.get(current_status, [])

    return new_status in allowed
