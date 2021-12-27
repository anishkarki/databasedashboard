from .layouts import main_layout_header, main_layout_sidebar

from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

from .__version__ import __version__
from .utils import get_dash_args_from_flask_config

def create_flask(config_object=f".settings"):
    """Create the Flask instance for this application"""
    server = Flask(__name__)
    server.config.from_object("databasedashboard.settings")
    return server

def create_dash(server):
    """Create the Dash instance for this application"""
    app = Dash(
        name=__name__,
        server=server,
        suppress_callback_exceptions=True,
        **get_dash_args_from_flask_config(server.config),


    )

    # Update the Flask config a default "TITLE" and then with any new Dash
    # configuration parameters that might have been updated so that we can
    # access Dash config easily from anywhere in the project with Flask's
    # 'current_app'
    server.config.setdefault("TITLE", "Dash")
    server.config.update({key.upper(): val for key, val in app.config.items()})

    app.title = server.config["TITLE"]

    if "SERVE_LOCALLY" in server.config:
        app.scripts.config.serve_locally = server.config["SERVE_LOCALLY"]
        app.css.config.serve_locally = server.config["SERVE_LOCALLY"]

    return app


# The Flask instance
server = create_flask()
# The Dash instance
app = create_dash(server)
# Push an application context so we can use Flask's 'current_app'
with server.app_context():
    # load the rest of our Dash app
    from . import index
    # configure the Dash instance's layout
    app.layout = main_layout_sidebar()
