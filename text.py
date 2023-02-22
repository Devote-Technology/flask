from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from transaction import createOriginalTransaction
from transaction import addReceiptUrl
import os

enviroment: str = os.environ.get("ENVIRONMENT")



def sendMessage(number, merchantName):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)


    if enviroment == "dev":
        companyNum = "+16506403459"
    else:
        companyNum = "+18019809310"
    

    
    sendMessage = "Please send a receipt of your recent purchase at " + merchantName 


    message = client.messages.create(
    body=sendMessage,
    from_= companyNum,
    to=number
    )

    print(message.sid)




def afterAuth(number, merchant, cardholderId, transactionId):

    createOriginalTransaction(transactionId=transactionId, cardholderId=cardholderId)
    sendMessage(number = number, merchantName=merchant["name"])
    

    return 
    #function that creates the transaction



def afterReceipt(image, number):
    addReceiptUrl(number=number, receiptURL=image)

    return 
    #figure out the transaction we need to change
    #upload that to db

