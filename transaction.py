from db import getConnection
import uuid




def createOriginalTransaction(transactionId, cardholderId):
  conn = getConnection()
  cur = conn.cursor()
  userId = getOwnerId(cardholderId=cardholderId, cur = cur)
  newId = str(uuid.uuid4())
  cur.execute("""
    INSERT INTO "Transaction" (id, "issuerID", "ownerId")
    VALUES (%s, %s, %s); 
  """, (newId, transactionId, userId))


  conn.commit()
  conn.close() 




def getOwnerId(cardholderId, cur):

  sql='SELECT * FROM "User" WHERE "cardholderID" = %s;'
  data=(cardholderId)
  cur.execute(sql, (data,))
  # cur.execute(sql)

  user = cur.fetchone()
  userId = user[0]
  print("userId: " + userId)
  return userId

# print(getOwnerId("ich_1MBk0LPuGEoJjTfqUkZDfYNW"))
# createOriginalTransaction("test2","ich_1MBk0LPuGEoJjTfqUkZDfYNW")


def addReceiptUrl(number, receiptURL): 
  conn = getConnection()
  cur = conn.cursor()
  ownerId = getOwnerIdFromNum(number=number, cur=cur)

  print("ownerID: " + ownerId)

  transactionId = getTransactionId(ownerId=ownerId, cur=cur)

  sql='UPDATE "Transaction" SET receipt = %s WHERE id = %s'

  cur.execute(sql, (receiptURL, transactionId ))
  conn.commit()

  conn.close()


#returns transaction that has receipt linked to text convo
def checkHasReceipt(number):
  conn = getConnection()
  cur = conn.cursor()
  ownerId = getOwnerIdFromNum(number=number, cur=cur)

  transactionID = getTransactionId(ownerId=ownerId, cur=cur)

  conn.close()

  return transactionID
  

def addTaxToTransaction(transactionId, tax):
  conn = getConnection()
  cur = conn.cursor()
  
  sql='UPDATE "TRANSACTION" SET tax = % WHERE id = %s'

  cur.execute(sql, (tax, transactionId))

  conn.close()

  return True



def getOwnerIdFromNum(number, cur):
  sql='SELECT * FROM "Card" WHERE "phoneNumber" = %s;'
  data=(number)
  cur.execute(sql, (data, ))
  owner = cur.fetchone()
  ownerId = owner[13]

  return ownerId


def getTransactionId(ownerId, cur):
  sql='SELECT * FROM "Transaction" WHERE "ownerId" = %s'
  data=(ownerId)
  cur.execute(sql, (data, ))
  transactions = cur.fetchall()
  #TODO: make sure it gets the right one
  transaction = transactions[-1]
  transactionId = transaction[0]
  

  return transactionId




# addReceiptUrl("+14806258657", "fakeURL")
  






