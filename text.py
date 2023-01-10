from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os



def sendMessage(number, location, name):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client()

    companyNum = "+16506403459"


    message = client.messages.create(
    body="Please send a receipt and memo of your recent purchase",
    from_= companyNum,
    to=number
    )