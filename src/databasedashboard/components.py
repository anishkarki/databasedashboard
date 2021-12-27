import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import current_app as server

from .utils import get_url, component


def fa(className):
    """A convenience component for adding Font Awesome icons"""
    return html.I(className=className)


@component
def make_brand(**kwargs):
    print(kwargs)
    return html.Header(
        className="brand",
        children=dcc.Link(
            href=get_url(""),
            children=html.H1([fa("far fa-chart-bar"), server.config["TITLE"]]),
        ),
        **kwargs,
    )


@component
def make_header(**kwargs):
    return dbc.Navbar(
        id="header",
        className="sticky-top",
        color="dark",
        width="auto",
        dark=True,
        children=[
            make_brand(),
            html.Ul(
                id=server.config["NAVBAR_CONTAINER_ID"], className="navbar-nav ml-auto"
            ),
        ],
        **kwargs,
    )


@component
def make_sidebar(**kwargs):
    return html.Nav(
        id=f"sidebar",
        children=[
            make_brand(),
            dbc.Nav(id=server.config["NAVBAR_CONTAINER_ID"])
        ],
        style={ "position": "fixed", "background": "black"},

        **kwargs,
    )

'''
sidebar= html.Div(
    [
        dbc.Nav(
            id="sidebar",
            children=[make_brand(), html.Div(id=server.config["NAVBAR_CONTAINER_ID"])],
            vertical = True,
            pills = True,
        ),
    ],
    style = SIDEBAR_STYLE,
)
'''