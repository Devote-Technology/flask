from flask import Flask, jsonify, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
import urllib.request
import stripe
import json
# from supabase import create_client, Client
from twilio.rest import Client
from text import *
import os
import threading
from transaction import checkHasReceipt, addTaxToTransaction




app = Flask(__name__)




# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(url, key)
db: str = os.environ.get("DB_NAME")
user: str = os.environ.get("DB_USER")
password: str = os.environ.get("DB_PASSWORD")
host: str = os.environ.get("DB_HOST")
port: str = os.environ.get("DB_PORT")
enviroment: str = os.environ.get("ENVIRONMENT")
webhook_secret: str = os.environ.get("WEBHOOK_SECRET")
stripe_key: str = os.environ.get("STRIPE_KEY")

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = stripe_key



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
        print (e)
        return ("Invalid signature", 400)

    if event["type"] == "issuing_authorization.created":

        if event["data"]["object"]["approved"] == True:
            print(event)

            number = event["data"]["object"]["card"]["cardholder"]["phone_number"]
            merchant = event["data"]["object"]["merchant_data"]
            transactionId = event["data"]["object"]["id"]
            metadata = event["data"]["object"]["card"]["cardholder"]["metadata"]

            cardholderId = event["data"]["object"]["cardholder"]

            #maybe cardID
            #pass in entire merchant data
            # ... custom business logic
            #not sure what we want to check for here

            thread = threading.Thread(target=afterAuth, args=(number, merchant, cardholderId, transactionId, metadata))
            thread.start()

            return 200, {"Stripe-Version": "2022-08-01", "Content-Type": "application/json"}

        
        #sendMessage(number=, location=) we need to call this with the correct information.
    #TODO: FIGURE OUT THE WHAT IS PASSED TO Up    


    #TODO: See if transaction is approved




    

    





#pushing to development

#most likely will get cardID from

@app.route('/receive', methods = ['GET', "POST"])
def receive():
    resp = MessagingResponse()
    numMedia = int(request.form['NumMedia'])
    number = request.form['From']



    if numMedia == 1:
        msg = resp.message("Thank you! Please send another text with the amount of sales tax in this format, 3.74.")
        imageUrl = request.form['MediaUrl0']
        


        print(imageUrl, number)
        # sendReceipt(request.form['MediaUrl0'])

        # thread = threading.Thread(target=afterReceipt, args=(imageUrl, number))
        # thread.start()

        afterReceipt(image=imageUrl, number=number)

        #function that uploads media url
        

    else:

        body = request.form['Body']
        try:
            tax = float(body)
            actualTax = int(tax * 100)
            # thread = threading.Thread(target=addTaxToTransaction, args=(number, actualTax))
            # thread.start()
            addTaxToTransaction(number=number, tax=actualTax)
            msg = resp.message("Perfect!")

            return str(resp)

        except:
            msg = resp.message("Please send the sales tax again with this format: 3.76")
    

    return str(resp)




if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
