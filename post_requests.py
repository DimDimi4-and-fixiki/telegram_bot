import requests
import time


class PostRequestMaker(object):
    """
    class for sending request to the server currently with the particular interval
    """
    def __init__(self, **kwargs):
        """
        :params:
            interval: int   interval to wait in seconds
            url:      str   url to send POST request
        """
        self.interval = kwargs.get("interval", 600)
        self.url = kwargs.get("url")
        self.make_request_on_interval()

    def make_request_on_interval(self):
        while True:
            self.make_request()
            time.sleep(self.interval)

    def make_request(self):
        my_data = {}
        print("REQUEST IS MADE")
        res = requests.post(url=self.url, data=my_data)


