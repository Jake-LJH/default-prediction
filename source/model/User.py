from model.DatabasePool import DatabasePool
from config.Settings import Settings
import jwt
import datetime
import bcrypt

class User:

    @classmethod
    def registerUser(cls,username, email, password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            password = password.encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())

            sql = "INSERT into user(username, email, password) values(%s,%s,%s)"   
            cursor.execute(sql,(username, email, hashed))
            dbConn.commit()
            recordCount = cursor.rowcount
            print(cursor.lastrowid)
            return recordCount
        finally: 
            dbConn.close()
    

    @classmethod
    def deleteUser(cls,userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "DELETE from user WHERE id = %s"   
            cursor.execute(sql,(userid,))
            dbConn.commit()

            recordCount = cursor.rowcount
            return recordCount
        finally: 
            dbConn.close()

    @classmethod
    def loginUser(cls,userJSON):
        try:
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f"Connected to {db_Info}")

            print(userJSON)
            cursor = dbConn.cursor(dictionary=True)
            sql = "select * from user where email=%s"

            cursor.execute(sql,(userJSON["email"],))
            user = cursor.fetchone() 
            if user==None:
                return {"jwt":""}

            else:
                
                password = userJSON["password"].encode()
                hashed = user['password'].encode()
                print(password)
                print(hashed)
                if bcrypt.checkpw(password, hashed):#True means valid password 
                    payload={"userid":user["id"],"username":user["username"],"email":user["email"],"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)}

                    jwtToken=jwt.encode(payload,Settings.secretKey,algorithm="HS256")
                    return {"jwt":jwtToken}
                else:
                    return {"jwt":""}
        finally:
            dbConn.close()

