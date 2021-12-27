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
                    "Vertica Daily Tasks",
                    id="collapse-button-vertica",
                    className="btn btn-primary btn-lg btn-block",
                    color="primary",
                    n_clicks=0,
                    ),
                dbc.Collapse(
                    mt.get_layout_mysqltasks(),
                    id="collapse-vertica",
                    is_open=False,
                    ),
            ],
        ),
    ],
)
@app.callback(
    Output("collapse-vertica", "is_open"),
    [Input("collapse-button-vertica", "n_clicks")],
    [State("collapse-vertica", "is_open")],
)
def toggle_collapse_vertica(n, is_open):
    if n:
        return not is_open
    return is_open

