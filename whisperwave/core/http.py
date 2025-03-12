import requests

class RequestHandler:
    def __init__(self, url):
        self.url = url
        self.payload = {}
        self.headers = {}

    def get(self):
        response = requests.request("GET", self.url, headers=self.headers, data=self.payload)
        return response.json()
    