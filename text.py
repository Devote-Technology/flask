from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from transaction import createOriginalTransaction
from transaction import addReceiptUrl
import os



def sendMessage(number, merchantName):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    

    companyNum = "+16506403459"
    sendMessage = "Please send a receipt of your recent purchase at " + merchantName 


    message = client.messages.create(
    body=sendMessage,
    from_= companyNum,
    to=number
    )

    print(message.sid)




def afterAuth(number, merchant, cardholderId, transactionId):

    sendMessage(number = number, merchantName=merchant["name"])
    createOriginalTransaction(transactionId=transactionId, cardholderId=cardholderId, merchantName = merchant["name"])

    #function that creates the transaction



def afterReceipt(image, number):
    addReceiptUrl(number=number, receiptURL=image)
    #figure out the transaction we need to change
    #upload that to db

