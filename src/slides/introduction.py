# necessary imports - do not change, and include on every slide
import dash_html_components as html
from app import app
import dash_core_components as dcc
import dash_bootstrap_components as dbc

###

content = html.Div(style = dict(textAlign='center'), children=[

    dbc.Card(style = dict(backgroundColor ='#e8f4ff', marginTop ="6rem"), children = [
    dbc.Card(dbc.CardBody([
    html.Div([html.H4("Introduction")], className = 'py-2'),

    html.Div(style =dict(textAlign='left', fontSize = 17), children = [

    html.Div([html.P("  Artificial intelligence (AI) has long been used in various industries,\
             and even the conservative construction industry is trying to use it for control\
             and process optimization.")]),
    html.P("  Nevertheless, AI is still quite an exotic tool\
             for widespread use; its occasional application and slow implementation are likely\
             due to misunderstandings and misinterpretation of AI and Machine learning(ML).\
             Thanks to marketers and journalists, who often exaggerate the complexity\
             and capability of  machine learning algorithms, modern AI is  still far from self-learning\
             and self-developing intelligence."),
    html.P ("  ML is just a subset of AI, which is mainly\
             used for prediction and classification. Despite its complexity, ML provides\
             unique opportunities for cement producers : for example, predicting\
             cement quality. For the most part, engineers still\
             rely on rules of thumb and do calculations manually in EXCEL. ML makes it\
             possible to predict cement quality more accurately, avoiding human factors.\
             There is no need to be an IT genius. Training a model involves one line of\
             Python code or a node in a Knime app. The parameter selection, data cleaning,\
             analysis, and model tuning are much more complex because they require knowledge\
             of cement production, statistics, and the ML paradigm."),
    html.P("There are a plethora of articles and discussions about machine learning\
            used to predict cement quality but as yet never a complete\
            application online. Pursuing ML certification, I created this\
            WEB application to demonstrate what different models predict\
            using a real dataset and apply it to the cement additives business.")

   ])  ], ))  ], className = 'shadow-lg p-3  rounded')
])
