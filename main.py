from flask import Flask, jsonify, request, session
from twilio.twiml.messaging_response import MessagingResponse
import urllib.request
import psycopg2
# from supabase import create_client, Client
from twilio.rest import Client
import os

app = Flask(__name__)

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
# supabase: Client = create_client(url, key)
db: str = os.environ.get("DB_NAME")
user: str = os.environ.get("DB_USER")
password: str = os.environ.get("DB_PASSWORD")
host: str = os.environ.get("DB_HOST")
port: str = os.environ.get("DB_PORT")


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


conn = psycopg2.connect(database=db, user = user, password = password, host = host, port = port)


@app.route('/transaction', methods = ['GET', 'POST'])
def approveTransaction():
    #TODO: FIGURE OUT THE WHAT IS PASSED TO US

    #TODO: See if transaction is approved

    approved = True

    if approved:
        print(approved)
        #TODO: Send an okay response
        #TODO: send the text messsage 

    else:
        #TODO: send not approved response

    




def sendMessage(number):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client()

    companyNum = "+16506403459"


    message = client.messages.create(
    body="Please send a receipt and memo of your recent purchase",
    from_= companyNum,
    to=number
    )



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

    
    supabase.storage().from_("receipt").upload("test1.png", image)
    
    #upload image to db somehow



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
