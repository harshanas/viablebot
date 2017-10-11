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
                Inc.database.add_user(user_data['id'],
                                     user_data['first_name'], user_data['last_name'],
                                     user_data['locale'], user_data['timezone'], user_data['gender'])
                Inc.messenger.send_message(data[1], {"text": "Hey "+user_data['first_name']+",\nI'm Grillo. What's up?"})

            nearby_matches = Inc.grillo.find_nearby_matches()
            if len(nearby_matches) >= 1:
                message = {"attachment":{"type":"template","payload":{"template_type":"generic","elements":[]}}}
                Inc.messenger.send_message(data[1], {"text": "There are several matches coming up"})
                for match in nearby_matches:
                    match_name = match['team-1']+" vs "+match['team-2']
                    element = {"title":match_name,
                               "subtitle":"Date: "+match['date'].split("T")[0],
                               "buttons":[{"type":"postback","title":"Get Alerts","payload":"GetAlerts_"+str(match['unique_id'])}]}
                    message['attachment']['payload']['elements'].append(element)
                Inc.messenger.send_message(data[1], message)

        elif "bye" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "Bye!"})
        elif "get_score" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "You said get score"})
        elif "teams" in witai_req_entities:
            Inc.messenger.send_message(data[1], {"text": "You said teams!"})

    def respond_to_payload(self, data):
        splitted_payload = data[2].split("_")

        if splitted_payload[0] == "GetAlerts":
            match_details = Inc.grillo.get_match_details(splitted_payload[1])
            if Inc.database.add_match(data[1],{"unique_id":splitted_payload[1], "date":match_details['date'].split("T")[0]}):
                Inc.messenger.send_message(data[1], {"text":"Added"})
            else:
                Inc.messenger.send_message(data[1], {"text": "Already Added"})