import Inc


class Response:
    def respond(self, data, witai_req=""):
        if data[0] == "text":
            self.respond_to_text(data, witai_req)
        elif data[0] == "payload":
            self.respond_to_payload(data)

    def respond_to_text(self, data, witai_req):
        witai_req_entities = witai_req['entities']
        user_data = Inc.messenger.get_user_profile(sender_id=data[1])
        if "greetings" in witai_req_entities and witai_req_entities['greetings'][0]['confidence'] > 0.9:

            if Inc.database.is_user_exist(sender_id=data[1]):
                Inc.messenger.send_message(data[1], {"text": "Hey "+user_data['first_name']+"!\n What do you like to find today?"})
            else:
                Inc.database.add_user(user_data['id'])
                Inc.messenger.send_message(data[1], {"text": "Hey "+user_data['first_name']+",\nHi, Harshana! I'm Viable. I can give the best places around you to buy  any sustainable alternative ."})

        elif "bye" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "Bye!"})
        elif "alternatives" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "Can I get your location please?","quick_replies":[{
                "content_type":"location"}]})
        elif "items" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "You said items!"})

    def respond_to_payload(self, data):
        Inc.messenger.send_message(data[1], {"text":"Out of 5 how many stars you like to give?","quick_replies":[
      {
        "content_type":"text",
        "title":"⭐⭐⭐⭐⭐",
        "payload":"FIVERATE"
      },
            {
                "content_type": "text",
                "title": "⭐⭐⭐⭐",
                "payload": "FOURRATE"
            },
            {
                "content_type": "text",
                "title": "⭐⭐⭐",
                "payload": "THREERATE"
            },
            {
                "content_type": "text",
                "title": "⭐⭐",
                "payload": "TWORATE"
            },
            {
                "content_type": "text",
                "title": "⭐",
                "payload": "ONERATE"
            }
    ]})

    def respond_to_location(self,data):
        stores = Inc.database.get_store(str(data[2]['lat']), str(data[2]['long']))
        print(stores)
        store_count = 0

        elements = []
        for store in stores:

            store_element = {"title": store[1],
                             "subtitle": store[3],
                             "buttons": [
                                 {
                                     "type": "web_url",
                                     "url": "https://petersfancybrownhats.com",
                                     "title": "View Google Maps"
                                 }, {
                                     "type": "postback",
                                     "title": "Rate this",
                                     "payload": "DEVELOPER_DEFINED_PAYLOAD"}]
                             }
            elements.append(store_element)
        payload = {"attachment": {"type": "template", "payload": {"template_type": "generic", "elements": elements}}}
        Inc.messenger.send_message(data[1], payload)