import os

class Settings:
    secretKey = '6w2hj*2nk4nfa089ym35\)anm52845-sreva124@$)(*17'

    #Dev
    
    #host='localhost'
    #database='creditcard'
    
    #user='root'
    #password='password'
    #password ="password"

    #Staging on heroku
    host=os.environ['HOST']
    database=os.environ['DATABASE']
    user=os.environ['USER']
    password=os.environ['PASSWORD']