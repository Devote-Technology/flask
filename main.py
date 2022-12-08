from flask import Flask, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse

import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/receive', methods = ['GET', "POST"])
def receive():
    resp = MessagingResponse()

    

    numMedia = int(request.form['NumMedia'])


    if numMedia == 1:
        msg = resp.message("Thank you for the receipt!")
        print(request.form['MediaUrl0'])

    else:
        msg = resp.message("Please send 1 picture of the Receipt")



    
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
