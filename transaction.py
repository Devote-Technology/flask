from db import getConnection
import uuid




def createOriginalTransaction(transactionId, cardholderId):
  conn = getConnection()
  cur = conn.cursor()
  userId = getOwnerId("ich_1MBk0LPuGEoJjTfqUkZDfYNW", cur)
  newId = str(uuid.uuid4())
  #get ownerId
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
  return userId

# print(getOwnerId("ich_1MBk0LPuGEoJjTfqUkZDfYNW"))
# createOriginalTransaction("test2","ich_1MBk0LPuGEoJjTfqUkZDfYNW")


def addPhoneNumber(number): 
  print("hello")





