from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os



def sendMessage(number, merchant):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client()

    companyNum = "+16506403459"

    sendMessage = "Please send a receipt of your recent purchase at " + merchant


    message = client.messages.create(
    body=sendMessage,
    from_= companyNum,
    to=number
    )