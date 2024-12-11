import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd
import numpy as np

author_name = 'Oumar KEITA'
# Application dash
app = dash.Dash()

data = pd.read_csv('/Users/mac/Documents/My_Dashboard/bank.csv')
job_proportion = data['job'].value_counts(normalize = True).sort_values(ascending = False)*100
refusal_rate_per_job_cat = data[data['deposit'] == 'no']['job'].value_counts(normalize = True)*100
refusal_per_month = data[data['deposit'] == 'no']['month'].value_counts(normalize = True)*100


marital_status = data['marital'].value_counts(normalize= True).sort_values(ascending = False)*100
marital_fig = px.bar(data_frame = marital_status, x = marital_status.index, y = marital_status.values, title = 'Proportion of marital status of the survey', color = marital_status.index)
refusal_job = px.bar(data_frame = refusal_rate_per_job_cat, x = refusal_rate_per_job_cat.values, y = refusal_rate_per_job_cat.index, 
                     color = refusal_rate_per_job_cat.index, title = 'Refusal rate per job category')
refusal_month = px.pie(data_frame = refusal_per_month, values = refusal_per_month.values, names = refusal_per_month.index,
                       title = 'Refusal rate per month')

#figure pour la proportion des jobs
job_prop_fig = px.bar(data_frame = job_proportion, x = job_proportion.index, y = job_proportion.values,
                      title = 'Job proportions of the survey', color = job_proportion.index)

age_dist = px.histogram(data_frame = data, x = 'age', title = 'Age distribution', nbins = 10)
balance_dist = px.histogram(data_frame = data, x = 'balance', title = 'balance distribution', nbins = 5)
duration_hist = px.histogram(data_frame = data, x = 'duration', title = 'Duration of call during last campaign', nbins = 10)

my_annotations = {'text': 'Management was the most represented job', 'x': 'management', 'y':22.9887117, 'showarrow': True,
                  'arrowhead': 1}

job_prop_fig.update_layout({'xaxis': {'title': 'Diffrent jobs'}, 'yaxis': {'title': 'Proportion in %'}, 'paper_bgcolor': 'lightgreen',
                            'plot_bgcolor': 'lightgreen'})
marital_fig.update_layout({'xaxis': {'title':'Martial Status'}, 'yaxis' : {'title':'Proportion in %'}, 'paper_bgcolor': 'lightgreen', 'plot_bgcolor': 'lightgreen'})
age_dist.update_layout({'xaxis': {'title': 'Age'},'paper_bgcolor': 'lightgreen', 'plot_bgcolor': 'lightgreen'})
balance_dist.update_layout({'xaxis':{'title':'Balance'}, 'paper_bgcolor': 'lightgreen', 'plot_bgcolor':'lightgreen'})
duration_hist.update_layout({'xaxis':{'title':'Duration in second(s)'}, 'paper_bgcolor':'lightgreen', 'plot_bgcolor':'lightgreen'})
refusal_job.update_layout({'yaxis':{'title':'Different jobs'}, 'xaxis':{'title':'Proportion in %'}, 'paper_bgcolor': 'lightgreen', 'plot_bgcolor':'lightgreen'})
refusal_month.update_layout({'paper_bgcolor':'lightgreen'})

app.layout = html.Div(children = [
    html.H1('Bank Marketing Data Analysis', style = {'text-align':'center'}),
    html.Div(children = [dcc.Graph(id = 'age_dist', figure = age_dist)], style = {'width':'400px', 'display':'inline-block'}),
    html.Div(children = [dcc.Graph(id = 'job_prop_bar', figure = job_prop_fig)], style = {'width':'500px', 'display':'inline-block', 'margin':'0px auto'}),
    html.Div(children = [dcc.Graph(id = 'marital_status', figure = marital_fig)], style = {'width':'400px', 'display':'inline-block', 'margin':'0px 0px 0px 20px'}),
    html.Br(),
    html.Div(children = [dcc.Graph(id = 'balance_dist', figure = balance_dist)], style={'width':'450px', 'display':'inline-block', 'margin':'0px 0px 0px 10px'}),
    html.Div(children = [dcc.Graph(id = 'duration_dist', figure = duration_hist)], style = {'width':'400px', 'display':'inline-block'}),
    html.Div(children = [
      #html.H4('Select a job', style = {'width':'200px', 'text-align':'center'}),
      dcc.Dropdown(id = 'refusal_per_marital',
                   options = [{'label': 'married', 'value':'married'},
                              {'label':'single', 'value': 'single'}, 
                              {'label': 'divorced', 'value':'divorced'}],
                   placeholder='Select a status', style = {'width':'300px'}
                   ),
      dcc.Graph(id = 'refusal_rate', style = {'width':'350px', 'color': 'lightgreen'})  
    ], style = {'display': 'inline-block', 'width': '400px','margin': '30px 0px 0px 20px'}),
    html.Br(),
    html.Div(children = [dcc.Graph(figure = refusal_job)], style =  {'width':'500px','display':'inline-block'}),
    html.Div(children = [dcc.Graph(id =  'refusal_month', figure = refusal_month)], style = {'width':'490px','display':'inline-block'}),
    html.Div(children = [
        dcc.Dropdown(id = 'housing_dropdown',
                      options = [{'label': 'Received housing loan', 'value':'yes'},
                                 {'label':"Didn't received housing loan", 'value':'no'}],style = {'width':'300px'},
                      placeholder= 'Select a housing category'),
        dcc.Graph(id = 'housing_graph', style = {'width':'350px', 'color': 'lightgreen'})
    ], style ={'width':'200px','display': 'inline-block'}),
    html.Br(),
    html.Span(children=[
            "This app was developed by: ", html.B(author_name),
            html.Br(),
            html.I("Last year master student at EMINES - School of Industrial Management/UM6P")
        ], style={'display': 'inline-block', 'margin-top': '20px'}),
        
        # Lien LinkedIn
        html.Span(children=[
            'My LinkedIn: ', 
            html.A('Oumar_KEITA_linkedin', 
                   href='https://www.linkedin.com/in/oumar-keita-a04374245/', 
                   target='_blank',  # Ouvre le lien dans un nouvel onglet
                   style={'color': 'blue', 'textDecoration': 'none'}),
        ], style={'display': 'inline-block', 'margin-top': '0px', 'margin-left': '300px'})
],
    style={'background-color': 'lightgreen', 'color': 'black','font-size':22, 'margin':'0 auto'},

)

@app.callback(
    Output(component_id = 'refusal_rate', component_property = 'figure'),
    Input(component_id = 'refusal_per_marital', component_property = 'value')
)

def update_plot(choose) :
    marital_stat = 'All the status'
    new_data = data.copy(deep = True)
    refusal = new_data[new_data['deposit'] == 'no']['marital'].value_counts(normalize=True)
    refusal_rate = px.pie(data_frame= refusal, values = refusal.values, names = refusal.index, title = 'Refusal rate per marital status')
    
    if choose : 
        marital_stat = choose
        new_data = new_data[new_data['marital'] == marital_stat]
        refusal = new_data['deposit'].value_counts()
        refusal = refusal.reindex(['no', 'yes'])
        refusal_rate = px.pie(data_frame= refusal, values = refusal.values, names = refusal.index, 
                              title = 'Refusal rate per marital status')
    refusal_rate.update_traces(sort=False)
    refusal_rate.update_layout({'paper_bgcolor': 'lightgreen'})
    
    return refusal_rate

@app.callback(
    Output(component_id= 'housing_graph', component_property = 'figure'),
    Input(component_id = 'housing_dropdown', component_property = 'value')
)

def update_housing(selection) :
    housing = 'All the category'
    housing_data = data.copy()
    housing_value = housing_data['housing'].value_counts(normalize = True)
    housing_graph = px.bar(data_frame = housing_value, x = housing_value.index, y = housing_value.values, 
                           title = 'Housing loan proportion of the survey', color = housing_value.index)
    if selection :
        housing_data = housing_data[housing_data['housing'] == selection]
        housing_deposit = housing_data['deposit'].value_counts(normalize = True)
        housing_deposit = housing_deposit.reindex(['no', 'yes'])
        if selection == 'yes' :
            housing_graph = px.pie(data_frame = housing_deposit, values = housing_deposit.values, names = housing_deposit.index,
                               title = "For people who received housing loan")
        else :
            housing_graph = px.pie(data_frame = housing_deposit, values = housing_deposit.values, names = housing_deposit.index,
                               title = "people who didn't receive housing loan")
            
    housing_graph.update_layout({'plot_bgcolor':'lightgreen', 'paper_bgcolor' : 'lightgreen'})
    return housing_graph


if __name__ == '__main__' :
    app.run_server(debug = True)
