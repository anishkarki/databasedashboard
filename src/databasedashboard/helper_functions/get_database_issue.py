import requests
import pandas as pd

df_issues = {}

def get_database_issues(dbtype):
    urlget = 'http://127.0.0.1:8000/databaseissuesinfo/{dbtype}'.format(dbtype=dbtype)
    data = requests.get(urlget)
    if data.json():
        df = pd.DataFrame.from_records(data.json()).sort_values(by=['issue_date'], ascending=False)
    else:
        df_issues['databasetype'] = [dbtype]
        df_issues['Issues'] = ['Issues not found']
        df = pd.DataFrame(df_issues) 
    return df
