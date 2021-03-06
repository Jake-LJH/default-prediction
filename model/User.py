from model.DatabasePool import DatabasePool
import bcrypt
from itsdangerous import URLSafeTimedSerializer
from config.Settings import Settings
import jwt
import datetime



class User:

    @classmethod
    def getUser(cls,userJSON):
        try:

            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql="select * from user where email=%s"
            cursor.execute(sql,(userJSON["email"],))
            user = cursor.fetchone()
            if user==None:
                return {"jwt":""}
            else:
                
                payload={"userid":user["id"],"username":user["username"],"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)}

                jwtToken=jwt.encode(payload,Settings.secretKey,algorithm="HS256")
                return {"jwt":jwtToken}

        finally:
            dbConn.close()

    @classmethod
    def insertUser(cls,name,email,password,organization,accType,role):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="insert into user(username,email,password,organisation,acc_type,role) values(%s,%s,%s,%s,%s,%s)"
            users = cursor.execute(sql,(name,email,password,organization,accType,role))
            dbConn.commit()
            rows = cursor.rowcount
            if rows > 0:
                
                create_result = True
                
                return create_result
            else:
                
                create_result = False
                return create_result
            
        except Exception as err:
            print(err)
            create_result = False
            return create_result
        finally:
            dbConn.close()




        

        





  
