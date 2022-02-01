import re
from enum import Enum

from messages.message import Message


class PollRequest(Enum):
    CREATE = {"prefix": "create a poll with options: ", "regex": "(\w+, )+\w+$"}
    VOTE = {"prefix": "vote #", "regex": "\d+ \w+$"}
    SHOW = {"prefix": "show results for poll ", "regex": "#\d+$"}


class Poll:

    def __init__(self, poll_number, options):
        self.poll_number = poll_number
        self.options: options
        self.results = {}
        for option in options:
            self.results[option] = 0


class Polls(Message):

    def __init__(self):
        super().__init__()
        self.poll_counter = 0
        self.polls = list()

        self.current_request = None
        self.current_request_input = None

    def is_valid_request(self, message):
        if not super().is_valid_request(message):
            return False
        message_without_prefix = message.partition(self.REQUEST_PREFIX)[2]
        for request in PollRequest:
            pattern = re.compile(request.value["prefix"] + request.value["regex"])
            if pattern.match(message_without_prefix):
                self.current_request = request
                self.current_request_input = message_without_prefix.partition(request.value["prefix"])[2]
                return True
        return False

    def execute_request(self, user_name, message):
        handle_requests = {PollRequest.SHOW: self._view_poll,
                           PollRequest.CREATE: self._create_poll,
                           PollRequest.VOTE: self._vote_in_poll}
        handler = handle_requests.get(self.current_request)(self.current_request_input)

    def _create_poll(self, poll_request):
        self.polls.append(Poll(self.poll_counter, poll_request.split(', ')))
        return self.RESPONSE_PREFIX + f"pol {self.poll_counter} created"

    def _vote_in_poll(self, poll_request):
        vote_request = poll_request.split(' ')
        if 0 < vote_request[0] < len(self.polls):
            self.polls[vote_request[0]].results[vote_request[0]] += 1
        return self.RESPONSE_PREFIX + f"poll number '{vote_request[0]}' does not exist"

    def _view_poll(self, poll_request):
        pass
