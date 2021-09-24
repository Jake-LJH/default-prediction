from os import system
#from model.DatabasePool import DatabasePool 
import pickle
from io import BytesIO
import pandas as pd
from flask import Flask, render_template, url_for, request, send_file
import os


class Prediction:
    
    @classmethod
    def getPredicted(cls,data,filename,upload_path):
    
        prediction_model = pickle.load(open("cc_model.pkl","rb"))
        default_predict = prediction_model.predict(data)
        default_predict_prob = prediction_model.predict_proba(data)

        if default_predict != "":

            prob = []
            data['default_result'] = default_predict

            for i in range(len(data['default_result'])):
                prob.append(default_predict_prob[i][data['default_result'].iloc[i]])
            data['probability'] = prob
            
            writer = pd.ExcelWriter(os.path.join(upload_path, filename), engine='xlsxwriter')
            data.to_excel(writer, sheet_name='Sheet1')
            writer.save()

            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            
            writer.close()      
        
        return data  
        '''
        send_file(output,
                     attachment_filename='predictionresult.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True)  ''' 