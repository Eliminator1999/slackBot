import requests
from messages.message import Message


class Weather(Message):
    REQUEST_PREFIX = "what’s the current weather in "
    RESPONSE_TEMPLATE = "It’s currently {} in {}, temperature is {} degrees celsius."
    WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
    CITY_NOT_FOUND_MESSAGE = "city: '{}' not found"

    def __init__(self):
        super().__init__()

    def is_valid_request(self, message):
        if not super().is_valid_request(message):
            return False

        return self.REQUEST_PREFIX in message

    def execute_request(self, user_name, message):
        city = message.partition(self.REQUEST_PREFIX)[2][:-1]
        weather = requests.get(url=self.WEATHER_API_URL,
                               params=dict(q=city, units="metric", APPID="4ceb17102ceeef616f980682627f7e32"))
        if weather.status_code != requests.codes.ok:
            return super().RESPONSE_PREFIX.format(user_name) + self.CITY_NOT_FOUND_MESSAGE.format(city)
        return self.respond_to_request(user_name, weather.json())

    def respond_to_request(self, user_name, message):
        return super().RESPONSE_PREFIX.format(user_name) + self.RESPONSE_TEMPLATE.format(message["weather"][0]["main"],
                                                                                         message["name"],
                                                                                         message["main"]["temp"])
