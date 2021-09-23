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
from model.Graph import Graph
from model.User import User
from werkzeug.utils import secure_filename
from flask.helpers import send_from_directory
import os


app = Flask(__name__)
CORS(app)
#app.config['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LEGTH'] = 1024 * 1024
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx']

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
            accountType = request.form['accType']

            if cpassword != password: #password check if same
                return render_template("createAccount.html",message="Passwords does not match")
            else:    
                create_result = User.insertUser(name,email,password,organization, accountType)
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
    return render_template('default_prediction.html')


@app.route('/default_prediction', methods = ['GET','POST'])
def default_prediction():
    print('yes')
    if request.method == 'POST':
        
        f = request.files['file']
        
        #saving file 
        file_name = secure_filename(f.filename)
        if file_name != "":
            file_ext = os.path.splitext(file_name)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
        
            file_xl = pd.read_excel(f,index_col=0)
            data = pd.DataFrame(file_xl)
            #data['TOT_PAY_STATUS']=data['PAY_0']+data['PAY_2']+data['PAY_3']+data['PAY_4']+data['PAY_5']+data['PAY_6']
            data=data[['PAY_0','BILL_AMT1','AGE','LIMIT_BAL','BILL_AMT2','BILL_AMT3','BILL_AMT4','PAY_AMT1','PAY_AMT2','PAY_AMT3']]
    

            default_predict = Prediction.getPredicted(data,f.filename,app.config['UPLOAD_PATH'])
            predicted_table = pd.DataFrame(default_predict[['AGE','BILL_AMT1','LIMIT_BAL','default_result', 'probability']])
            
            predicted_table.reset_index(inplace=True)
            pngImageB64String=Graph.generatePieChart(predicted_table)
             # changin the prediction result values of 1 and 0 to yes and no
            predicted_table['default_result'] = ["yes" if x==1 else "No" for x in predicted_table['default_result']] 
            
    return render_template('main.html',f_name= f.filename, records=len(predicted_table), image=pngImageB64String, show_table=True, table = predicted_table) #table_id="predicted_result", .to_html( classes="table table-striped table-bordered table-sm")

            #htmlTable = df.to_html(classes="table table-bordered table-hover", justify='center', table_id='myTable', na_rep='-')

           # pngImageB64String=Graph.generatePieChart(df)
    #return render_template('main.html',f_name= f.filename, table = htmlTable, image=pngImageB64String, records=len(df))

@app.route('/<filename>/download_file')   
def download_file(filename)    :
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

#***** Adding the Default route ******

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
