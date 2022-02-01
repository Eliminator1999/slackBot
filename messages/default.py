from messages.message import Message


class Default(Message):
    RESPONSE_PREFIX = "Sorry @{}, I can’t process your request: '{}'"

    def __init__(self):
        super().__init__()

    def execute_request(self, user_name, message):
        return self.respond_to_request(user_name, message)

    def respond_to_request(self, user_name, message):
        return self.RESPONSE_PREFIX.format(user_name, message)
