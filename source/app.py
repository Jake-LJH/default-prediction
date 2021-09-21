from io import BytesIO
from logging import debug
from flask import Flask, render_template, url_for, request, send_file, abort
from flask.helpers import send_from_directory
from pandas.io import pickle
from werkzeug.utils import secure_filename
import json
import pandas as pd
import pickle
from pandas import ExcelWriter
import xlsxwriter
import jinja2 
from model.prediction import Prediction
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#app.config['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LEGTH'] = 1024 * 1024
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.xlsx']


@app.route('/')
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
            predicted_table = pd.DataFrame(default_predict[['LIMIT_BAL','default payment prediction', 'probability']])
            print("result",default_predict)
    return render_template('default_prediction.html',f_name= f.filename, predicted_table = predicted_table.to_html(classes="table table-striped table-bordered table-sm"))

@app.route('/<filename>/download_file')   
def download_file(filename)    :
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
if __name__ == '__main__':
    app.run(debug = True)
