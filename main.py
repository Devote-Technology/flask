from flask import Flask, jsonify, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
import urllib.request
import psycopg2
import stripe
import json
# from supabase import create_client, Client
from twilio.rest import Client
from text import *
import os
import threading



app = Flask(__name__)

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(url, key)
db: str = os.environ.get("DB_NAME")
user: str = os.environ.get("DB_USER")
password: str = os.environ.get("DB_PASSWORD")
host: str = os.environ.get("DB_HOST")
port: str = os.environ.get("DB_PORT")

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = 'sk_test_51LruhiLQhKtna1xjBrA0gz4hdt5Fpkrk1HIckTnYPiFbBbWmmIVYvDKUNQYexxRAQaOyKNH9rdTEtuTreclGALbr00eJvEOIjl'

# Uncomment and replace with a real secret. You can find your endpoint's
# secret in your webhook settings.
webhook_secret = 'whsec_ae2e9V6KIbrIR5ei6ph1jKjJSw9q52Xc'


#conn = psycopg2.connect(database=db, user = user, password = password, host = host, port = port)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


@app.route('/transaction', methods = ['GET', 'POST'])
def approveTransaction():

    print("here")

    request_data = json.loads(request.data) #not sure what this is.
    signature = request.headers.get("stripe-signature")

    # Verify webhook signature and extract the event.
    try:
        event = stripe.Webhook.construct_event(
        payload=request.data, sig_header=signature, secret=webhook_secret
        )
        print(event)
    except ValueError as e:
        # Invalid payload.
        return ("Invalid payload", 400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return ("Invalid signature", 400)

    if event["type"] == "issuing_authorization.request":
        auth = event["data"]["object"]
        # print("auth", auth)

        number = event["data"]["object"]["card"]["cardholder"]["phone_number"]
        merchant = event["data"]["object"]["merchant_data"]["name"]
        # ... custom business logic
        #not sure what we want to check for here

        thread = threading.Thread(target=sendMessage, args=(number, merchant))
        thread.start()

        return json.dumps({"approved": True}), 200, {"Stripe-Version": "2022-08-01", "Content-Type": "application/json"}


        #sendMessage(number=, location=) we need to call this with the correct information.
    #TODO: FIGURE OUT THE WHAT IS PASSED TO Up    


    #TODO: See if transaction is approved




    

    







#most likely will get cardID from

@app.route('/receive', methods = ['GET', "POST"])
def receive():
    resp = MessagingResponse()
    numMedia = int(request.form['NumMedia'])


    if numMedia == 1:
        msg = resp.message("Thank you for the receipt!")
        print(request.form['MediaUrl0'])
        # sendReceipt(request.form['MediaUrl0'])
        

    else:
        msg = resp.message("Please send 1 picture of the Reciept")

    return str(resp)


# def sendReceipt(link):

    
#     supabase.storage().from_("receipt").upload("test1.png", image)
    
#     #upload image to db somehow



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
