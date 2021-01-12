import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from corona.data import source
from corona.data.transform import *

app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

app.layout = html.Div(
  children=[
    html.Div(
      # left panel (option panel)
      className='col',
      style={'width': '100%', 'height': '100%'},
      children=[
        html.Div(
          className='four columns div-user-controls',
          children=[
            html.H1('COVID-19 tracking'),
            html.P('As of Jan 2021'),
            html.Div([
              dcc.Dropdown(
                id='mode',
                options=[
                  {'label': 'Case vs Recovery', 'value': 'cvr'},
                  {'label': 'Test vs Case', 'value': 'tvc'},
                  {'label': 'Case vs Health care capacity', 'value': 'cvcap'},
                  {'label': 'Case vs Vaccination', 'value': 'cvv'}
                ],
                value='cvr'
              )
            ]),
            html.Div(
              style={'margin-top': '10px'},
              children=[
                dcc.Dropdown(
                  id='country',
                  options=[
                    {'label': 'Germany', 'value': 'Germany'},
                    {'label': 'France', 'value': 'France'},
                    {'label': 'UK', 'value': 'United Kingdom'},
                    {'label': 'USA', 'value': 'United States'},
                    {'label': 'China', 'value': 'China'},
                    {'label': 'Thailand', 'value': 'Thailand'}
                  ],
                  value=['Germany', 'Thailand'],
                  multi=True
                )
            ]),
            html.Div(
              style={'margin-top': '10px'},
              children=[
                dcc.Dropdown(
                  id='tick',
                  options=[
                    {'label': 'Daily', 'value': 'd'},
                    {'label': 'Weekly', 'value': 'w'},
                    {'label': 'Monthly', 'value': 'm'},
                  ],
                  value='d',
                  multi=False
                )
            ])
          ]
        ), 
        html.Div(
          # Right panel (graph display)
          className='one columns div-user-controls',
          children=[
            dcc.Graph(id='display')
          ]
        ),
      ])
  ])

# Data on memory
df_covid19 = source.read_covid19_data()

def get_aggregator(mode):
  aggr = {
    'cvr': {'new_cases': 'sum'},
    'tvc': {'total_tests_per_thousand': 'sum'},
    'cvcap': {'weekly_icu_admissions': 'sum'},
    'cvv': {'new_vaccinations': 'sum'}
  }
  return aggr[mode]

# Bind UI callbacks 
@app.callback(
  Output(component_id='display', component_property='figure'),
  Input(component_id='mode', component_property='value'),
  Input(component_id='country', component_property='value'),
  Input(component_id='tick', component_property='value'))
def refresh_display(mode, country, tick):
  print('-------------------------------')
  print(f'Selected mode    : {mode}')
  print(f'Selected country : {country}')
  return plot_agg(
    df=df_covid19,
    country_list=country,
    period=tick,
    aggregator=get_aggregator(mode))




if __name__ == '__main__':
    print(df_covid19[5:])
    app.run_server(debug=True)