from db import getConnection
import uuid




def createOriginalTransaction(transactionId, cardholderId, merchantName):
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

  transactionId = getTransactionId(number=number, cur=cur)

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
  

def addTaxToTransaction(number, tax):
  
  conn = getConnection()
  cur = conn.cursor()
  transactionID = getTransactionId(number=number, cur=cur)
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
  sql="""
  SELECT "Transaction".id from "Transaction"
  inner join "Card"
  ON "Transaction"."cardholderID" = "Card"."cardHolderID"
  where "Card"."phoneNumber" = %s
  ORDER BY "Transaction"."createdAt" ASC
  """
  data=(number)
  cur.execute(sql, (data, ))
  transactions = cur.fetchall()
  print(transactions)
  #TODO: make sure it gets the right one
  transaction = transactions[-1]
  print(transaction)
  transactionId = transaction[0]
  

  return transactionId




#addTaxToTransaction("+14806258657", 96)
#createOriginalTransaction("heloajfd", "ich_1MBk0LPuGEoJjTfqUkZDfYNW", "target")

  






