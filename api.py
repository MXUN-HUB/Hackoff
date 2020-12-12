import requests
import json
import plotly
import plotly.express as px
import plotly.graph_objs as go


api = requests.get('https://api.covid19india.org/data.json')
api_state = api.json()['statewise']
api_cases_time_series = api.json()['cases_time_series']
api_tested = api.json()['tested']

dailyconfirmed = [] 
date = []

for j in api_cases_time_series:
    dailyconfirmed.append(j['dailyconfirmed'])
    date.append(j['date'])


deaths = []
state = []


for i in api_state:
    deaths.append(i['deaths'])
    state.append(i['state'])


def create_plot():
    data=[go.Scatter(x=x, y=y, mode='lines+markers')]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
