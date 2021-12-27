import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
import sys
sys.path.append("..")
from ..app import app

from ..helper_functions import mysqltasks as mt

layout = html.Div(
    [
        dbc.Container(
            fluid=True,
            children = [
                dbc.Button(
                    "Postgres Daily Tasks",
                    id="collapse-button-postgres",
                    className="btn btn-primary btn-lg btn-block",
                    color="primary",
                    n_clicks=0,
                    ),
                dbc.Collapse(
                    mt.get_layout_mysqltasks(),
                    id="collapse-postgres",
                    is_open=False,
                    ),
            ],
        ),
    ],
)
@app.callback(
    Output("collapse-postgres", "is_open"),
    [Input("collapse-button-postgres", "n_clicks")],
    [State("collapse-postgres", "is_open")],
)
def toggle_collapse_postgres(n, is_open):
    if n:
        return not is_open
    return is_open

