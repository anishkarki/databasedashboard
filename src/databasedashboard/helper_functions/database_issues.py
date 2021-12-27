import pandas as pd
import dash_bootstrap_components as dbc
from ..helper_functions import get_database_issue as gdi

df_issues = pd.DataFrame(
    {
        ("Score", "Max"): {
            "Arthur Dent": 6.0,
            "Ford Prefect": 4.0,
            "Zaphod Beeblebrox": 1.0,
            "Trillian Astra": 3.0,
        },
        ("Score", "Average"): {
            "Arthur Dent": 2.0,
            "Ford Prefect": 2.0,
            "Zaphod Beeblebrox": 0.7,
            "Trillian Astra": 1.9,
        },
    }
)

def mysql_issues():
    df = gdi.get_database_issues('mysql')
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, index=True)

def postgres_issues():
    df = gdi.get_database_issues('postgres')
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, index=True)

def vertica_issues():
    df = gdi.get_database_issues('vertica')
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, index=True)