import requests

# A Slack service to set
class Slack:

    __URL     = None
    __CHANNEL = None

    #Sets Webhook URL on itiilization
    def __init__(self, url):
        self.__URL = url

    # A function to set the channel. Users may want to invoke this class several times with different channels.
    def setChannel(self,channel):
        self.CHANNEL = channel
    
    # A function to post a message in the format:
    # <Handle>: <Content>
    def postToSlack(self, user, message):
        payload = {}
        payload['text'] = user + ": " + message
        payload["channel"] = self.__CHANNEL
        res = requests.post(self.__URL, json=payload)
        try:
            res.raise_for_status()
        except res.exceptions.HTTPError as e:
            return "Error: " + str(e)

        # Success
        print(res.text)