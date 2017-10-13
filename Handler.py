import Inc


class Handler:

    def handle_post_request(self, request):
        json_request = request.json
        print(json_request)

        if 'channelId' in json_request:
            if json_request['channelId'] == "facebook":
                data = Inc.messenger.recieve_message(json_request)
                handled_message = self.handle_messages(data)
                Inc.response.respond(data, handled_message)

        return "", 200

    def handle_get_request(self, request):
        print(request.json)
        return "", 200

    def handle_messages(self, data):
        if data[0] == "text":
            # send it to witai, get result, return it, send it to response module
            witai_request = Inc.witai.understand(data[2])
            return witai_request
        elif data[0] == "coordinates":
            Inc.response.respond_to_location(data)
