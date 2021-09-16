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


app = Flask(__name__)

#app.config['UPLOAD_FOLDER']
#app.config['MAX_CONTENT_PATH']


@app.route('/upload_file')
def upload_file():
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
        data['TOT_PAY_STATUS']=data['PAY_0']+data['PAY_2']+data['PAY_3']+data['PAY_4']+data['PAY_5']+data['PAY_6']
        data['BILL_AMT1_OVER_LIMIT_BAL']=data['BILL_AMT1']/data['LIMIT_BAL']
    
        prediction_model = pickle.load(open("credit_card_default_random_forest_trainedby_class_imbalance_using_undersampling.pkl","rb"))
        default_predict = prediction_model.predict(data)
        print("prediction",default_predict)
        
        if default_predict != "":
            data['default payment prediction'] = default_predict
            
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            data.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            #output_file.seek(0)
            print(data)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            
            writer.close()
            #with ExcelWriter("prediction.xlsx") as writer:
            
            output.seek(0) 
             #   predicted_xl = data.to_excel(writer)
        print("predictedfile",workbook)
        msg ="success"
        
    return send_file(output,
                     attachment_filename='predictionresult.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True)       
        
if __name__ == '__main__':
    app.run(debug = True)