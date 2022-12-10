from flask import Flask, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse
import urllib.request
from supabase import create_client, Client
from dotenv import load_dotenv


import os

app = Flask(__name__)

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


#most likely will get cardID from

@app.route('/receive', methods = ['GET', "POST"])
def receive():
    resp = MessagingResponse()
    numMedia = int(request.form['NumMedia'])


    if numMedia == 1:
        msg = resp.message("Thank you for the receipt!")
        print(request.form['MediaUrl0'])
        sendReceipt(request.form['MediaUrl0'])
        

    else:
        msg = resp.message("Please send 1 picture of the Reciept")

    return str(resp)


def sendReceipt(link):

    image = urllib.request(link)
    supabase.storage().from_("receipt").upload("test.png", image)
    
    #upload image to db somehow



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
