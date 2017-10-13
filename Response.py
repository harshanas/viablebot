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
                Inc.messenger.send_message(data[1], {"text": "Hey Harshana!"})
            else:
                Inc.database.add_user(user_data['id'])
                Inc.messenger.send_message(data[1], {"text": "Hey "+user_data['first_name']+",\nI'm Grillo. What's up?"})

        elif "bye" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "Bye!"})
        elif "get_score" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "You said get score"})
        elif "teams" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "You said teams!"})

    def respond_to_payload(self, data):
        splitted_payload = data[2].split("_")

        if splitted_payload[0] == "RateStore":
            print('Rates the store')