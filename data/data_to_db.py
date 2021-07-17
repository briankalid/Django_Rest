# from Plerk.settings import settings
import pandas as pd
from datetime import datetime
# import Company
# from Company.models import company
import sqlite3
from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('../db.sqlite3')

        print("Connection successful")

        return con

    except Error:

        print(Error)

if __name__ == '__main__':
    pars_date = lambda x: str(x[0:19])

    db = pd.read_csv('test_database.csv',parse_dates=['date'],date_parser=pars_date)

    db.dropna(inplace=True)


    db['company'] = db['company'].apply(lambda x: x.capitalize())

    """
    company = models.CharField(max_length=100)
    price = models.FloatField()
    date = models.DateTimeField()
    status_transaction = models.CharField(max_length=50)
    status_approved = models.BooleanField()
    """

    con = sql_connection()

    try:
        db.to_sql('Company_company',con=con, if_exists='append',index=False)

    except Error:
        print(Error)

    finally:
        con.close()
