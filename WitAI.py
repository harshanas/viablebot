import requests
import datetime
import urllib.parse
import json


class WitAI:
    def __init__(self, access_token):
        self.date = datetime.datetime.now().strftime ("%d/%m/%Y")
        self.url = "https://api.wit.ai/message?v="+self.date+"&q="
        self.access_token = access_token

    def understand(self, text):
        headers = {'Authorization': 'Bearer '+self.access_token}
        text_encoded = urllib.parse.quote_plus(text)
        url = self.url+text_encoded
        print(url)
        request = requests.get(url, headers=headers)
        print(request.text)
        return json.loads(request.text)
