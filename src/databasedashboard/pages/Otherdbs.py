from collections import Counter
from textwrap import dedent
import sys
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
import pandas as pd
import dash_table
import requests

from ..app import app
from ..helper_functions import database_issues as di
from ..helper_functions import database_value_featch as dvf


def get_layout(**kwargs):
    initial_text = kwargs.get("text", "Type some text into me!")
    # Note that if you need to access multiple values of an argument, you can
    # use args.getlist("param")
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Mysql Issues", tab_id="mysql-issues"),
                    dbc.Tab(label="Postgres Issues", tab_id="postgres-issues"),
                    dbc.Tab(label="Vertica Issues", tab_id="vertica-issues"),
                ],
                id="tabs",
                active_tab="mysql-issues",
            ),
            html.Div(id="content"),
            html.Br(),
            html.H2("Database Information Dashboard"),
            dash_table.DataTable(
                id = 'table-filtering-be',
                columns = [{"name": i, "id": i} for i in sorted(dvf.get_database_status().columns)],
                filter_action = "native",
                filter_query = '',
                page_current = 0,
                page_size = 20,
                page_action = "native",
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
            html.Br(),
            html.H2("Database Backup Dashboard"),
            dash_table.DataTable(
                id='table-filtering-backup',
                columns=[{"name": i, "id": i} for i in sorted(dvf.get_database_backup_status().columns)],
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

        ]
    )

operators = [['ge ', '&ge;'], ['le ', '&le;'], ['lt ', '&lt;'], ['gt ', '&gt;'], ['ne ', '&ne;'], ['eq ', '='], ['contains '], ['datestartswith ']]
def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                return name, operator_type[0], value
    return [None] * 3

@app.callback(
    Output('table-filtering-be', 'data'),
    [Input('table-filtering-be', "filter_query")],
)
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    dff = dvf.get_database_status()
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
    return dff.to_dict('records')

@app.callback(
    Output('table-filtering-backup', 'data'),
    [Input('table-filtering-backup', "filter_query")],
)
def update_table(filter):
    filtering_expressions = filter.split(' && ')
    dff = dvf.get_database_backup_status()
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
    return dff.to_dict('records')



@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def callback(input_value):
    return 'Output: {}'.format(input_value)


@app.callback(Output("content", "children"), [Input('tabs', 'active_tab')])
def switch_tab(at):
    if at == 'mysql-issues':
        return di.mysql_issues()
    elif at == 'postgres-issues':
        return di.postgres_issues()
    elif at == 'vertica-issues':
        return di.vertica_issues()
    else:
        return html.P("This shouldn't ever be displayed...")