#! /bin/usr/python3

from flask import Flask
from flask import request
import Handler

app = Flask(__name__)
handler = Handler.Handler()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return handler.handle_post_request(request)
    else:
        return handler.handle_get_request(request)

if __name__ == '__main__':
    app.run()
