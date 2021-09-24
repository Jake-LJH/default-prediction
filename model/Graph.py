from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
import random
import io
import numpy as np
import pandas as pd

class Graph:
    
    @classmethod
    def generatePieChart(cls,data):
    
        # Generate plot
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        #fig.suptitle('Credit Card Default Prediction Chart', fontsize=17)
        axis.axis('equal')
        status = ['No Default', 'Default']
        

        no_default_0 = len(data[data['default_result'] == 0])
        default_1 = len(data[data['default_result'] == 1])
        proportion = [no_default_0,default_1]
        
        def func(pct, allvalues):
            absolute = round(pct / 100.*np.sum(allvalues))
            return "{:.1f}%\n({:d})".format(pct, absolute)

        axis.pie(proportion, labels = status,radius=1.4,textprops={'fontsize': 17},autopct = lambda pct: func(pct, proportion))

        fig.tight_layout()

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        
        return pngImageB64String  

    @classmethod
    def generateProbabilityPieChart(cls,data):
    
        # Generate plot
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.axis('equal')
        #fig.suptitle('Defaulter Probability Distribution', fontsize=17)
        
        # retrieve all the predicted defaulters
        default_1 = data[data['default_result'] == 1]
        default_1['probability'] = pd.to_numeric(default_1['probability'], downcast="float")

        #Create 2nd pie chart grouped by probability
        prob9to1 = len(default_1.loc[(default_1['probability'] >= 0.9)])
        prob8to9 = len(default_1.loc[(default_1['probability'] >= 0.8) & (default_1['probability'] < 0.9)])
        prob7to8 = len(default_1.loc[(default_1['probability'] >= 0.7) & (default_1['probability'] < 0.8)])
        prob6to7 = len(default_1.loc[(default_1['probability'] >= 0.6) & (default_1['probability'] < 0.7)])
        prob5to6 = len(default_1.loc[(default_1['probability'] >= 0.5) & (default_1['probability'] < 0.6)])

        #labels for the pie chart
        labels = ['0.9 and above', '0.8 - 0.9', '0.7 - 0.8','0.6 - 0.7','0.5 - 0.6']
        probabilities = [prob9to1,prob8to9,prob7to8,prob6to7,prob5to6]

        def func(pct, allvalues):
            absolute = round(pct / 100.*np.sum(allvalues))
            return "{:.1f}%\n({:d})".format(pct, absolute)

        axis.pie(probabilities, labels = labels,radius=1.4,textprops={'fontsize': 17},autopct = lambda pct: func(pct, probabilities))            

        fig.tight_layout()

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        
        return pngImageB64String  
