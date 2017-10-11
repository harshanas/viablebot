import requests
import json


class Messenger:
    def __init__(self, page_access_token):
        self.url = "https://graph.facebook.com/v2.6/me/messages?access_token="
        self.graph_url = "https://graph.facebook.com/v2.6/"
        self.page_access_token = page_access_token
        self.message_url = self.url+self.page_access_token

    def recieve_message(self, request):
        channel_data = request['channelData']

        sender_id = channel_data['sender']['id']
        recipientId = channel_data['recipient']['id']
        if 'message' in channel_data:
            message_data = channel_data['message']
            if 'text' in message_data:
                return ['text', sender_id, message_data['text']]

        elif 'postback' in channel_data:
            message_data = channel_data['postback']
            return['payload', sender_id, message_data['payload']]




    def send_message(self, sender_id, message):
        message_obj = {"recipient": {"id": sender_id}, "message": message}
        request = requests.post(self.message_url, json=message_obj)
        print(message_obj)
        print(request.status_code, request.text)

    def get_user_profile(self, sender_id):
        url = self.graph_url+sender_id+"?fields=first_name,last_name,locale,timezone,gender&access_token="+self.page_access_token
        request = requests.get(url)
        return request.json()

#messenger = Messenger("EAABwnDx3fvQBAJN1uGNKK7KVyNKPTZCblYHFl2Q3ZAR3XarbFPS44ruxgAMbUdg97Ve6B3ddBlcDuHikOoFPi9qOlMlM3y92ZB8wVDRZCckn6znlJR2sY9TX0PSmYEsHo9Cla09rwmWBTUMhdGRoErCRPqzfZCCwTZCpIwLTXdcMiLXHP12Ivg")
#print(messenger.get_user_profile("1282168675226359"))