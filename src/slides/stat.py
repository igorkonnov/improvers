import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from sklearn.metrics import mean_squared_error, max_error, mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

import app
from utils import get_pandas_data
from utils import model_list

df1= get_pandas_data('data.csv')
so3 = df1= get_pandas_data('data2.csv')


Z2 =so3[['R 008, %','SO₃, %', 'additive1, g/t', 'additive2, g/t',
 't, cement, ° С', 'moisture,%', 'Free_lime,%',
       'limestone,%', 'Eq.Na2O,%', 'C3S%', 'C3A%', 'LOI,%']]
Y2 = so3['2 days MPa']
Z1 =df1[['R 008, %','SO₃, %', 'additive1, g/t', 'additive2, g/t',
't, cement, ° С', 'moisture,%', 'Free_lime,%',
       'limestone,%', 'Eq.Na2O,%', 'C3S%', 'C3A%', 'LOI,%']]
Y = df1['2 days MPa']
modeldataframe = pd.DataFrame({'model': []})
model_list( Z1, Y)
modeldataframe['model'] = model_list(Z1, Y)
x_train, x_test, y_train, y_test = train_test_split(Z1, Y, test_size=15,
 random_state=42)

def score1(x):
    return round(x.score(x_test, y_test),2)
def mse(x):
    return round( mean_squared_error(x.predict(x_test),y_test),2)
def maxe(x):
    return  round(max_error(x.predict(x_test),y_test),2)
def mabse(x):
    return  round(mean_absolute_error(x.predict(x_test),y_test),2)
def cvs (x):
    return round(cross_val_score ( x , Z1 , Y, cv =5).mean(),2)

modeldataframe['r_squared'] = modeldataframe['model'].apply(score1)
modeldataframe['mean_squared_error'] = modeldataframe['model'].apply(mse)
modeldataframe['max error'] = modeldataframe['model'].apply(maxe)
modeldataframe['mean_absolute_error'] = modeldataframe['model'].apply(mabse)
modeldataframe['cross-validation score'] = modeldataframe['model'].apply(cvs)


modeldata1 = modeldataframe
modeldata1['model']= ['Ridge regression',  'HistGradientBoosting regression',
 'Huber', 'Lasso', 'ExtraTreesRegressor' ]

content = html.Div(style=dict(textAlign='center', border='1px'),children=[


    html.H2(id='intro-div'),

    html.Br(),html.Hr([], className = "divider py-0.5 mb-4 bg-primary"),
    html.Div([html.H4('What is a "machine learning model?"')], className ='py-2'),
    html.Div([
         dbc.Card( dbc.CardBody([

    html.P("A machine learning model(ML) is a file that has been trained to\
            recognize certain types of patterns.The dataset is devided by\
            trained and test samples and 5 MLs have been trained.\
            Predictors - selected cement quality parameters, target variable\
            (predicted variable)- 2 days cement compressive\
            strength.", style = dict(textAlign ="left"))]) ) ]),


    html.Div([html.H6("How precise is this prediction?")], className ="row mx-auto py-2"),
    html.Div([html.P("Metrics are used to monitor and measure the performance\
     of a model.")], className = "row py-2 mx-auto"),


    html.Div([html.H6("This is the ML performance metrics")], className = "row py-2 mx-auto"),

    html.Div([dash_table.DataTable(data = modeldata1.to_dict("records"),
    columns =  [{"id": c, "name": c, "selectable": True} for c in
      modeldata1.columns],
    style_header={ "backgroundColor": "#1E90FF", "color": "white",'textAlign': 'center',
    "fontSize": "8pt" },fixed_rows={"headers": True},style_cell={"width": "90px",
    "fontSize": "10pt",'textAlign': 'center'} )], className = "py-2"),
    html.Div([html.P("*cross validation score - 5-fold average cross validation score")], className='row mx-auto'),


    html.Div([
        dbc.Card(
           dbc.CardBody(style = dict(textAlign="left"), children =[html.P(
           "Ridge model demonstrated the best accuracy and performance,\
           lower MSE and higher coefficient of determination. Such ML models like Ridge, Huber, and\
           Lasso are perfect for predicting linear processes. Since the relationship\
           between predictors and dependent variables is very close to linear,\
           these models are ideal for prediction. Of course, nothing is linear in\
           real life. With extreme values (e.g., SO3 > 4%), models like Gradient Booster\
           demonstrated better performance. So, ideally, you will use a combination\
           of two models, such as Ridge Regression and Gradient Boosting. Gradient\
           Boosting requires a bigger dataset, but Linear regression models are\
                  good for a small dataset. " )

        ]))], className = 'py-2' ),

    html.Div([html.H5('Ml models limitations')]),
    html.Div([html.P("Example: how do the different models predict 2D strength during 'SO3 optimization?'")], className = 'row py-2 mx-auto'),
    html.Div([html.H6("Select a model to see predicted and actual values")],className = 'row py-2 mx-auto'),

    html.Div([
        dcc.Dropdown(
            id='models',
            options=[{'label': i, 'value': i} for i in modeldata1['model']],
            value='Ridge regression'
        ),
    ], className = 'py-2'),
    html.Div([dcc.Graph(id = 'so3optimization')]),

    html.P("The linear models do not predict non-linear process. HistGradientBoosting requires more data to train")


])


@app.app.callback(
    Output('so3optimization', 'figure'),
    Input('models', 'value'))

def so3opt(models):
    fig = px.scatter(Z2, x = 'SO₃, %', y = Y2)
    fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left", x=0.01))
    u = modeldata1['model'].to_list().index(models)
    fig.add_trace(go.Scatter(x= Z2['SO₃, %'],y=model_list(Z2,Y2)[u].predict(Z2),
    mode='markers',
    marker=dict(
        size=4,
       color='red',
        symbol='4'
      ),
        name='predicted 2D MPa'
      ), secondary_y= False)
    fig.update_xaxes(title='SO3')
    fig.update_yaxes(title='2D compressive strength, MPa')
    return fig
