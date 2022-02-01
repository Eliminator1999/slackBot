from slack import RTMClient
from message_handler import get_response


class Bot:

    def __init__(self, channel_name: str, access_token: str) -> None:
        self.channel_name = channel_name
        self.access_token = access_token
        self.rtm_client = RTMClient(token=self.access_token)
        self.rtm_client.start()

    @RTMClient.run_on(event="message")
    def run(self, **payload):
        data = payload['data']
        if self.channel_name != data['channel']:
            return

        web_client = payload['web_client']

        response = get_response(data['user'], data['text'])

        web_client.chat_postMessage(
            channel=data['channel'],
            text=response,
            thread_ts=data['ts']
        )
