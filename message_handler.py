from messages.polls import Polls
from messages.weather import Weather
from messages.default import Default

SUPPORTED_MESSAGES = [Polls(), Weather()]


def get_response(user_name, message):
    for supported_message in SUPPORTED_MESSAGES:
        if supported_message.is_valid_request(message):
            return supported_message.execute_request(user_name, message)
    return Default().execute_request(user_name, message)
