# -*- coding: utf-8 -*-
"""
Created on Sun May 23 22:37:00 2021

@author: laura
"""

import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import chart_studio.plotly as py
import cufflinks as cf
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.offline import plot


#%% array de ejemplo

arr1 = np.random.randn(50,4)
df1 = pd.DataFrame(arr1, columns=['A', 'B', 'C', 'D'])


import plotly.graph_objects as go
df_stocks = px.data.stocks()

figura = px.line(df_stocks, x='date', y = 'GOOG', labels = {'x':'Date', 'y': 'stock of google'})

# para poder ver esa gráfica me toca usar algun tipo de html output

from plotly.offline import plot
plot(figura)


figura2 = px.line(df_stocks, x= 'date', y=['GOOG', 'AAPL'], labels = {'x': 'Fecha', 'y': 'Stocks value'} )

# figura2.write_image('ejemplo.png', engine= 'kaleido')

plot(figura2)



#%% LINEGRAPHS


df3 = sums_year[0]
df3.index
years = ['2019','2020','2021']
print(top3_name)

for i in range(3):
    df3 = sums_year[i]
    fig = px.line(df3, x= df3.index, y= principales_name, title=years[i])
    fig.write_html(years[i],'.html')
    plot(fig)
#%% PIECHARTS

dfk = anuales[0]
dfk = dfk[principales_name]
dfk = dfk.transpose()

dfk.columns = ['frec']


for i in range(len(years)):
    dfk = anuales[i]
    dfk = dfk[principales_name]
    dfk = dfk.transpose()
    dfk.columns = ['frec']
    fig = px.pie(dfk,values='frec', names=dfk.index, title=years[i])
    fig.write_html('piecahrt'+ years[i]+'.html')
    plot(fig)
    
    

#%% BARCHART DE SEGUNDA INSTANCIA

# uso mi tablita de gb5 que tiene index en los derechos principales y porcentajes de true y false
df5.columns = ['False', "True"]
fig = px.bar(df5, x=df5.index, y=["True", "False"], title="Wide-Form Input")
plot(fig)
