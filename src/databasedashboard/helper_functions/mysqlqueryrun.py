import pandas as pd
import mysql.connector
import os
import sys

def mysql_queryrun(query, db_name, db_user, db_pass, db_host):
    """
    This function takes a query, database name, database user, database password and database hostname and returns the results of the query as a pandas dataframe.
    """
    try:
        db_connection = mysql.connector.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        db_results = pd.read_sql(query, con=db_connection)
        return db_results,1
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return err,0

if __name__=='__main__':
    query = "SELECT * FROM mysql.user"
    db_name = "mysql"
    db_user = "root"
    db_pass = "my-secret-pw"
    db_host = "localhost"
    db_results, stat_code = mysql_queryrun(query, db_name, db_user, db_pass, db_host)
    print(db_results, type(db_results))