from io import BytesIO
from logging import debug
from flask import Flask, render_template, url_for, request, send_file, abort, make_response, redirect
from pandas.io import pickle
from werkzeug.utils import secure_filename
import json
import pandas as pd
import pickle
from pandas import ExcelWriter
import xlsxwriter
import jinja2 
from flask_cors import CORS
from model.prediction import Prediction
from model.User import User


app = Flask(__name__)
CORS(app)
#app.config['UPLOAD_FOLDER']
#app.config['MAX_CONTENT_PATH']

@app.route('/verify', methods= ['POST']) #route for login.html submit button
def verifyUser():
    
        email = request.form['email']
        password = request.form['password']
        Jusers=User.getUser(email,password)

        print(Jusers)

        if Jusers == 0:
            return render_template('login.html',message="Invalid Login Credentials")

        else:
            return render_template('default_prediction.html')

@app.route('/signup') #new user page render 
def signup():
    return render_template("createAccount.html") 

@app.route('/newUser', methods=['GET','POST']) #create new user account
def newUser():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            organization = request.form['organization']
            password = request.form['password']
            cpassword = request.form['cpassword']   
            #AccountType = request.form['accType']

            if cpassword != password: #password check if same
                return render_template("createAccount.html",message="Passwords does not match")
            else:    
                create_result = User.insertUser(name,email,password,organization)
                if create_result == True: 
                    return render_template('login.html',message="New User Created") #create new user response
                else:    
                    return render_template('login.html',message="User email already exists") #fail to create new user notification
        else:
            return render_template("login.html")
    except Exception as err:
        print(err)
        return render_template('signup.html',message="an error occured")


@app.route('/predict') #direct route for prediction page
def upload_file():
    # test commit
    return render_template('default_prediction.html')

@app.route('/default_prediction', methods = ['GET','POST'])
def default_prediction():
    print('yes')
    if request.method == 'POST':
        
        f = request.files['file']
        print(f)
        print("here")
        file_xl = pd.read_excel(f,index_col=0)
        data = pd.DataFrame(file_xl)
        #data['TOT_PAY_STATUS']=data['PAY_0']+data['PAY_2']+data['PAY_3']+data['PAY_4']+data['PAY_5']+data['PAY_6']
        data=data[['PAY_0','BILL_AMT1','AGE','LIMIT_BAL','BILL_AMT2','BILL_AMT3','BILL_AMT4','PAY_AMT1','PAY_AMT2','PAY_AMT3']]
    
        #prediction_model = pickle.load(open("cc_model.pkl","rb"))
        default_predict = Prediction.getPredicted(data)
        
        
    return default_predict   

# ***** Adding the Default route ******

@app.route('/<string:url>')
def staticPage(url):
    print("static page",url)
    try:
        return render_template(url)
    except Exception as err:
        print(err)
        abort(404)

@app.route('/')
def login():
    try:
        return redirect("login.html")
    except Exception as err:
        abort(404)

@app.route('/logout') #define the api route
def logout():
    resp = make_response(redirect("login.html"))
    resp.delete_cookie('jwt')
    
    return resp

# ***** Error Handling ******

@app.errorhandler(404)
def page_not_found(e):
    
    return render_template('404.html'), 404





if __name__ == '__main__':
    app.run(debug = True)