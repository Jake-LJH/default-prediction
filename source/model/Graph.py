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
        #axis.set_title("Credit Card Default Prediction Chart")
        #axis = fig.add_axes([0,0,1,1])
        axis.axis('equal')
        status = ['No Default', 'Default']

        no_default_0 = len(data[data['default_result'] == 0])
        default_1 = len(data[data['default_result'] == 1])
        proportion = [no_default_0,default_1]
        #axis.pie(proportion, labels = status,autopct='%1.2f%%')
        #autopct=lambda p: '{:.0f}%'.format(p * total / 100),
        def func(pct, allvalues):
            absolute = int(pct / 100.*np.sum(allvalues))
            return "{:.1f}%\n({:d})".format(pct, absolute)

        axis.pie(proportion, labels = status,autopct = lambda pct: func(pct, proportion))

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        
        return pngImageB64String  


