from io import BytesIO
from logging import debug
from flask import Flask, render_template, url_for, request, send_file
from pandas.io import pickle
from werkzeug.utils import secure_filename
import json
import pandas as pd
import pickle
from pandas import ExcelWriter
import xlsxwriter
import jinja2 
from model.prediction import Prediction


app = Flask(__name__)

#app.config['UPLOAD_FOLDER']
#app.config['MAX_CONTENT_PATH']


@app.route('/')
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
        
if __name__ == '__main__':
    app.run(debug = True)