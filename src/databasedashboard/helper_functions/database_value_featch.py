import requests
import pandas as pd

def get_database_status():
    data = requests.get('http://127.0.0.1:8000/databaseinfo/')
    df = pd.DataFrame.from_records(data.json()).sort_values(by=['entrytime'], ascending=False)
    return df

def get_database_backup_status():
    data_backup = requests.get('http://127.0.0.1:8000/databaseback/')
    df_backup = pd.DataFrame.from_records(data_backup.json()).sort_values(by=['created'], ascending=False)
    return df_backup

