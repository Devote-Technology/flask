from db import getConnection
import uuid
import stripe

import os

stripe_key: str = os.environ.get("STRIPE_KEY")

stripe.api_key = stripe_key






def createOriginalTransaction(transactionId, cardholderId):
  conn = getConnection()
  cur = conn.cursor()
  orgId = getOrgId(cardholderId=cardholderId, cur = cur)
  newId = str(uuid.uuid4())
  cur.execute("""
    INSERT INTO "Transaction" (id, "stripeTxID", "cardholderID", "createdAt", "organizationId", "updatedAt")
    VALUES (%s, %s, %s, now(), %s, now()); 
  """, (newId, transactionId, cardholderId, orgId))


  conn.commit()
  conn.close() 




def getOrgId(cardholderId, cur):

  sql='SELECT * FROM "User" WHERE "cardholderID" = %s;'
  data=(cardholderId)
  cur.execute(sql, (data,))

  user = cur.fetchone()
  orgId = user[9]
  return orgId

# print(getOwnerId("ich_1MBk0LPuGEoJjTfqUkZDfYNW"))
# createOriginalTransaction("test2","ich_1MBk0LPuGEoJjTfqUkZDfYNW")


def addReceiptUrl(number, receiptURL): 
  conn = getConnection()
  cur = conn.cursor()

  transaction = getTransactionId(number=number, cur=cur)

  transactionId = transaction[0]

  connectID = getConnectId(transaction[2], cur)

  stripe.issuing.Authorization.modify(
  transaction[1],
  metadata = {"receiptURL" : receiptURL},
  stripe_account= connectID
  )



  sql='UPDATE "Transaction" SET receipt = %s WHERE id = %s'

  cur.execute(sql, (receiptURL, transactionId ))
  conn.commit()

  conn.close()


#returns transaction that has receipt linked to text convo
def checkHasReceipt(number):
  conn = getConnection()
  cur = conn.cursor()
  ownerId = getOwnerIdFromNum(number=number, cur=cur)

  transaction = getTransactionId(ownerId=ownerId, cur=cur)

  transactionID = transaction[0]

  conn.close()

  return transactionID
  

def addTaxToTransaction(number, tax):
  
  conn = getConnection()
  cur = conn.cursor()
  transaction = getTransactionId(number=number, cur=cur)

  transactionID = transaction[0]

  connectID = getConnectId(transaction[2], cur)

  stripe.issuing.Authorization.modify(
    transaction[1],
    metadata = {"salesTax" : tax},
    stripe_account= connectID
  )

  sql='UPDATE "Transaction" SET tax = %s WHERE id = %s'

  cur.execute(sql, (tax, transactionID))
  conn.commit()

  conn.close()

  return True



def getOwnerIdFromNum(number, cur):
  sql='SELECT * FROM "Card" WHERE "phoneNumber" = %s;'
  data=(number)
  cur.execute(sql, (data, ))
  owner = cur.fetchone()
  ownerId = owner[13]

  return ownerId


def getTransactionId(number, cur):

  sql2 = """
  SELECT "cardholderID"
  from "Card"
  where "phoneNumber" = %s
  """

  data=(number)
  cur.execute(sql2, (data))
  cards = cur.fetchall()

  print(cards)

  
  # print(users)

  sql = """
  SELECT "Transaction".id, "Transaction"."stripeTxID", "Transaction"."organizationId"
  from "Transaction"
  WHERE "Transaction"."cardholderID" = %s; 
  """

  cardholderId = (cards[0][0])
  cur.execute(sql, (cardholderId, ))

  transactions = cur.fetchall()

  # sql="""

  # SELECT "Transaction".id, "Transaction"."stripeTxID", "Transaction"."organizationId"
  # from "Transaction"
  # inner join "Card"
  # ON "Transaction"."cardholderID" = "Card"."cardholderID"
  # where "Card"."phoneNumber" = %s
  # ORDER BY "Transaction"."createdAt" DESC;
  # """


  # data=(number)

 
  # cur.execute(sql, (data, ))
  # transactions = cur.fetchall()

  print(transactions)
  #TODO: make sure it gets the right one
  transaction = transactions[0]
  # stripeTxId = transaction[10]

  # print(stripeTxId + ": stripe id")
  

  return transaction


def getConnectId(orgId, cur):
  sql="""
  SELECT "connectAccountID"
  FROM "Organization"
  WHERE id = %s 
  """

  data=(orgId)
  cur.execute(sql, (data, ))
  connectIds = cur.fetchall()

  connectID = connectIds[0][0]

  return connectID
  
  




#addTaxToTransaction("+14806258657", 104)
#addReceiptUrl("+14806258657", "https://api.twilio.com/2010-04-01/Accounts/AC66756d2940b364773dfc21efc2a93152/Messages/MM79024cbdecbfed2ad70a156d92955204/Media/ME18c16571c5182bc9963c8e8dae83bd4f")
#createOriginalTransaction("heloajfd", "ich_1MBk0LPuGEoJjTfqUkZDfYNW", "target")

  






