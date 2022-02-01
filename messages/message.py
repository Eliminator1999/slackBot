class Message:
    REQUEST_PREFIX = "hey @bot, "
    RESPONSE_PREFIX = "hey @{}, "

    def __init__(self):
        pass

    def is_valid_request(self, message):
        if self.REQUEST_PREFIX not in message:
            return False
        return True

    def execute_request(self, user_name, message):
        pass

    def respond_to_request(self, user_name, message):
        return self.RESPONSE_PREFIX.format(user_name)
