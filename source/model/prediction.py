from os import system
#from model.DatabasePool import DatabasePool 
import pickle
from io import BytesIO
import pandas as pd
from flask import Flask, render_template, url_for, request, send_file


class Prediction:
    
    @classmethod
    def getPredicted(cls,data):
        prediction_model = pickle.load(open("cc_model.pkl","rb"))
        default_predict = prediction_model.predict(data)
        print(default_predict)
        if default_predict != "":
            print('yes')
            
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