# from Plerk.settings import settings
import pandas as pd
from datetime import datetime
# import Company
# from Company.models import company
import sqlite3
from sqlite3 import Error
import uuid

def sql_connection():

    try:

        con = sqlite3.connect('../db.sqlite3')

        print("Connection successful")

        return con

    except Error:

        print(Error)

def clean(df):

    df.dropna(inplace=True)


    df['company'] = df['company'].apply(lambda x: x.capitalize())
    df['date'] =df['date'].apply(lambda x : str(x[0:22]))

    df[df['company'] == 'Hbomax'] = 'Hbo max'
    df[df['company'] == 'Izzy internet'] = 'Izzi internet'
    df[df['company'] == 'Paramount pluss'] = 'Paramount+'
    df[df['company'] == 'Pedidos ya'] = 'Pedidosya'
    df[df['company'] == 'New york times'] = 'The new york times'

    return df

def companies_to_db(df, con):
    companies=df['company'].unique()
    companies = pd.DataFrame(companies,columns=['name'])
    companies['status'] = 'activa'
    companies['id']=None
    companies['id'] = companies['id'].apply(lambda x: str(uuid.uuid4()))

    try:
        companies.to_sql('Company_company',con=con, if_exists='append',index=False)

    except Error:
        print(Error)

    return companies

def transactions_to_db(df,companies,con):
    # print(df.columns, companies.columns)
    transactions = pd.merge(df,companies,left_on='company',right_on='name').drop(['name','company','status'],axis=1)
    transactions.rename(columns={'id':'company_id','date':'date_transaction'},inplace=True)
    transactions['id']=None
    transactions['id'] = transactions['id'].apply(lambda x: str(uuid.uuid4()))

    try:
        transactions.to_sql('Transaction_transaction',con=con, if_exists='append',index=False)

    except Error:
        print(Error)

if __name__ == '__main__':
    # pars_date = lambda x: str(x[0:22])

    # db = pd.read_csv('test_database.csv',parse_dates=['date'],date_parser=pars_date)
    db = pd.read_csv('test_database.csv')

    db = clean(db)

    con = sql_connection()

    companies=companies_to_db(db,con)

    transactions_to_db(db,companies,con)


    con.close()
