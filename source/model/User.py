from model.DatabasePool import DatabasePool
import bcrypt
from itsdangerous import URLSafeTimedSerializer
from config.Settings import Settings

secretKey="a12nc)238OmPq#cxOlm*a"
salt = 'assignment_two'

class User:

    @classmethod
    def getUser(cls,email,password):
        try:

            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql="select * from Account where email=%s"
            cursor.execute(sql,(email,))
            users = cursor.fetchone()
            print(type(users))
            print(users)

            hashed=users['password'].encode('utf8)')
            password=password.encode('utf8)')
             
            if bcrypt.checkpw(password, hashed):#True means valid password 
                return users

            else:
                users=0
                return users
        except:
            users=0
            return users

        finally:
            dbConn.close()
            print("release connection")

    @classmethod
    def insertUser(cls,name,email,password,organization):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        sql="select * from Account where email=%s" #checks for existing user
        cursor.execute(sql,(email,))
        row = cursor.fetchall()
        if len(row) == 0:

            userid=cursor
            password = password.encode('utf8')
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            print(password)
        
            sql="insert into Account(name,email,password,organization) Values(%s,%s,%s,%s)"
            users = cursor.execute(sql,(name,email,password,organization))
        
            dbConn.commit()
            rows=cursor.rowcount
            print(cursor.lastrowid)
            create_result=True
            dbConn.close()
            return create_result
        

        else:

            create_result=False
            dbConn.close()
            return create_result
          




        

        





  
