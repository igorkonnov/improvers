from app import app
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utils import model_list
import pandas as pd
from utils import get_pandas_data
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import HuberRegressor

import pathlib


df1= get_pandas_data('data.csv')

#df1 = pd.read_csv('data.csv', sep = ',')
Z1 =df1[['R 008, %','SO₃, %', 'additive1, g/t', 'additive2, g/t', 't, cement, ° С',
         'moisture,%', 'Free_lime,%','limestone,%', 'Eq.Na2O,%', 'C3S%', 'C3A%', 'LOI,%']]
Y = df1['2 days MPa']



content = html.Div(style=dict(textAlign='center', border='4px'),children=[
    html.H2(id='intro-div'),
    html.Br(),html.Hr([], className = "divider py-0.5 bg-primary"),
    html.Div([html.H4('Interactive application, different MLs and predicted 2d MPa\
                       compressive strength')], className ='py-2'),
    html.Div([html.H6('Enter parameters to get prediction : ')], className ="row ml-2"),
    html.Div([ dash_table.DataTable( id='table-editing-simple',
               data= Z1.head(1).to_dict('records'), columns=[{'id': p, 'name': p}
               for p in list(Z1.columns)], editable=True,
              style_header={ "backgroundColor": "#1E90FF",
                             "color": "white",'textAlign': 'center',"width": "70px"},
              fixed_rows={"headers": True},style_cell={"width": "90px",
                          "fontSize": "10pt",'textAlign': 'center'}
                     )
             ]),
    html.Div([html.Output(id='danger', style={'width': '20%', 'height': 8,
                             'font-size':15, 'margin-bottom':0, 'color': 'red' })]),
    html.Div([html.H6("Output, 2d predicted MPa:")], className ="row mb-3 ml-2"),
    html.Div([
    html.Div([
            dbc.Row([
                dbc.Col([html.Label("Ridge" )]),
                dbc.Col([html.Label("HG.Booster")]),
                dbc.Col([html.Label("HUBER")]),
                dbc.Col([html.Label("Lasso")]),
                dbc.Col([html.Label("ExtraTreesRegressor")])
                   ])
            ],className ='mb-2'),

    html.Div([
        dcc.Loading( children = [
         dbc.Row( [
            dbc.Col(dbc.Card( color="primary", outline=True, children = html.Output(id = 'ridge') )),
            dbc.Col(dbc.Card( color="primary", outline=True, children =html.Output(id = 'booster'))),
            dbc.Col(dbc.Card( color="primary", outline=True, children =html.Output(id = 'hoober'))),
            dbc.Col(dbc.Card( color="primary", outline=True, children =html.Output(id = 'lasso'))),
            dbc.Col(dbc.Card( color="primary", outline=True, children =html.Output(id = 'destree'))),
                 ], ),
             ])  ])
  ], ),
  html.Div([html.P('It is noted that in a real world cement plant environment the\
    variables are rarely outside a fairly tight well established range.\
    The upper and lower limits have been set based on realistic real\
     world values.')], className= 'row mt-4'),
   html.Br(),html.Hr([], className = "divider py-2 bg-primary"),
   html.Div([html.H6("How to measure the performance of cement additives with\
                      ML?")],className="mt-4"),
   html.Div(style = dict(textAlign='left'), children =[dbc.Card(dbc.CardBody([
             html.P("1.	Enter cement parameters of a sample treated with the additive,\
                    set additive dosage to zero-get the predicted compressive strength without additive."),
             html.P("2.	Compare the predicted quality and the actual quality of this\
                     cement sample treated with the additive. The difference is the\
                      additive performance. Consider the model accuracy.")
        ]))]),

   html.Div([html.H6("How to improve  the “Accuracy” of a Machine Learning Model")],className="py-2"),
   html.Div(style=dict(textAlign='left'),
         children =[dbc.Card(dbc.CardBody(
                        [html.P("1. More predictors usually provide better accuracy, but avoid or remove multicollinearity."),
                         html.P("2. PSD analysis can significantly improve the accuracy of prediction."),
                         html.P("3. Quality of data is essential – garbage in, garbage out. "),
                         html.P ("4. Bigger is a dataset – better is the prediction. "),
                         html.P(" 5. Some irregular  parameters like outdoor temperature,  water injection,\
                          % of open storage clinker can improve the prediction quality."), ]))])
])


@app.callback(
    Output ('ridge', 'children'),
    Output ('booster', 'children'),
    Output ('hoober', 'children'),
    Output ('lasso', 'children'),
    Output ('destree', 'children'),
    Output('danger', 'children'),
    Input('table-editing-simple', 'data'),
    Input('table-editing-simple', 'columns'))

def display_output(rows, columns):

    model_demonstration = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    model_demonstration = model_demonstration.astype('float')
    if  model_demonstration['R 008, %'][0] >4 or  model_demonstration['SO₃, %'][0] >4\
     or model_demonstration['additive1, g/t'][0] >1000 or  model_demonstration['additive2, g/t'][0] >500\
     or model_demonstration['t, cement, ° С'][0] > 130\
     or model_demonstration['Eq.Na2O,%'][0] > 1.5\
     or model_demonstration['moisture,%'][0] > 1  or model_demonstration['Free_lime,%'][0]>2 :

     danger = 'a value is out of range, no prediction available'
     return  0, 0, 0, 0, 0, danger

    elif  model_demonstration['additive1, g/t'][0]  and model_demonstration['additive2, g/t'][0] != 0 :
        danger = 'not possible to use 2 adds, no prediction'
        return  0, 0, 0, 0, 0, danger

    elif  model_demonstration['limestone,%'][0] > 5 :
        danger = "limestone above 5% is restricted by the standard"
        return  0, 0, 0, 0, 0, danger

    else :
        danger =''
        ridge = round(model_list(Z1, Y)[0].predict(model_demonstration).item(0),2)
        booster = round(model_list(Z1, Y)[1].predict(model_demonstration).item(0),2)
        huber = round(model_list(Z1, Y)[2].predict(model_demonstration).item(0),2)
        lasso = round(model_list(Z1, Y)[3].predict(model_demonstration).item(0),2)
        polinomal = round(model_list(Z1, Y)[4].predict(model_demonstration).item(0),2)
        return ridge, booster, huber, lasso, polinomal, danger
