import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
import sys
from ..app import app
from ..helper_functions import mysqlqueryrun as mst
import dash_table


query_run = html.Div([
    dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Label('Username: '),
        dcc.Input(id='username', type='text', placeholder='Username',className="inputbox1",style={'margin-left':'2%','width':'450px','height':'45px','padding':'2px','margin-top':'2px','font-size':'16px','border-width':'3px','border-color':'#a0a3a2'})
    ]),
    html.Div([
        dbc.Label('Password:'),
        dcc.Input(id='password', type='password', placeholder='Password', className="inputbox2",style={'margin-left': '2%', 'width': '450px', 'height': '45px', 'padding': '2px','margin-top': '2px', 'font-size': '16px', 'border-width': '3px','border-color': '#a0a3a2'})]
        ,style={'margin-bottom':'2px'}
    ),
    html.Div([
        dbc.Label('Hostname:'),
    dcc.Dropdown(
        id='hostname',
        options=[{'label': '127.0.0.1', 'value': 'localhost'}],
        value='localhost'
    )], style={'margin-bottom':'2px'}
    ),
    html.Div([
        dbc.Label("Database Name:"),
        dcc.Input(id='database_name', type='text', placeholder='Database name',className="inputbox3",style={'margin-left':'2%','width':'450px','height':'45px','padding':'2px','margin-top':'2px','font-size':'16px','border-width':'3px','border-color':'#a0a3a2'})
    ],style={'margin-bottom':'5px'}),
    html.Div(dcc.Textarea(
        id='textarea-example',
        value='',
        placeholder='Enter your query here',
        style={'width': '100%', 'height': 300},
    )),
    html.Div(html.Button('Run Query', id='run-query', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),style={'margin-left':'45%','padding-top':'5px'}),

]),
])

def get_searchtable(df, id):
    dtable = html.Div([
        dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in sorted(df.columns)],
        filter_action="native",
        filter_query='',
        page_current=0,
        page_size=20,
        page_action="native",
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Date', 'Region']
        ],
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        }
    ),
    ])
    return dtable


def get_layout_mysqltasks():
    layout = html.Div([
    # represents the URL bar, doesn't render anything
        html.Br(),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H3('Choose MySQL Tasks'),
                    dcc.Dropdown(
                        id='task-dropdown',
                        options=[
                            {'label': 'Create new user', 'value': 'CNU'},
                            {'label': 'Take a new backup', 'value': 'TNB'},
                            {'label': 'Run a query', 'value': 'RQ'},
                        ],
                        value='RQ'
                    ),
                    ],
                    width=3, style= {'border': '1px solid black','padding': '10px'}),
                dbc.Col(
                    html.Div(id='page-content1', style={'border': '1px solid black', 'padding': '10px'}),
                ),
            ]),
            html.Div(id='query-result', style={'margin-top': '20px', 'border': '1px solid black', 'padding': '10px'})
        ], fluid=True),
        # content will be rendered in this element
        dcc.Location(id='url1', refresh=False),
    ])
    return layout

@app.callback(Output('page-content1', 'children'),
              [
                  Input('task-dropdown', 'value'),
              ])
def display_page_button1(value):
    if value == 'CNU':
        return html.Div([
            html.H3('You are on page {}'.format(value))
        ])
    elif value == 'TNB':
        return html.Div([
            html.H3('You are on page {}'.format(value))
        ])
    elif value == 'RQ':
        return query_run

@app.callback(Output('query-result', 'children'),
              [
                  Input('run-query', 'n_clicks'),
                  Input('username', 'value'),
                  Input('password', 'value'),
                  Input('hostname', 'value'),
                  Input('database_name', 'value'),
                  Input('textarea-example', 'value')
              ])
def query_output(n_clicks, username, password, hostname, database, query):
    if n_clicks == 0:
        return 'No query has been run yet.'
    else:
        df, test = mst.mysql_queryrun(query=query, db_name=database, db_user=username, db_pass=password, db_host=hostname)
        return html.Div([
            dash_table.DataTable(id='table',columns=[{"name": i, "id": i} for i in df.columns],data=df.to_dict('records'),
                                 style_cell_conditional=[{'if': {'column_id': c}, 'textAlign': 'left'} for c in ['Date', 'Region']],style_data={'color': 'black', 'backgroundColor': 'white'},style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(220, 220, 220)'}],style_header={'backgroundColor': 'rgb(210, 210, 210)', 'color': 'black', 'fontWeight': 'bold'}
                                 ),
            ])


