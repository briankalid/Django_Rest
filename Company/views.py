# from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
import pandas as pd

# from Company import models, serializers
from Transaction.models import transaction
from django.core import serializers as parser
from rest_framework.views import APIView
# from django.core import serializers
import json
# from Transaction.models import transaction
from rest_framework import status
# Create your views here.
from django.db.models.query import QuerySet
#
class Resume(APIView):

    def get(self, request, format=None):
        query_companies = models.company.objects.all()
        query_transactions = transaction.objects.all()

        query_transactions_json = parser.serialize('json', query_transactions)

        query_transactions_json = json.loads(query_transactions_json)

        names=[company.name for company in query_companies]
        pks = [str(company.id) for company in query_companies]
        status = [company.status for company in query_companies]

        df_companies = pd.DataFrame([pks,names,status]).T
        df_companies.columns = ['id_company','Name','Status']

        id = [transaction.id for transaction in query_transactions]
        id_companies = [str(transaction['fields']['id_company']) for transaction in query_transactions_json]
        prices = [transaction.price for transaction in query_transactions]
        payments = [transaction.final_charge for transaction in query_transactions]

        df_transactions = pd.DataFrame([id,id_companies,prices,payments]).T
        df_transactions.columns = ['id','id_company','price','payment']

        transactions = pd.merge(df_transactions,df_companies,on='id_company')
        ventas=transactions.groupby(['Name','payment']).price.sum()
        ventas=ventas.reset_index()

        cobradas = ventas[ventas['payment'] == True]
        no_cobradas = ventas[ventas['payment'] == False]
        maximums = cobradas.sort_values(by='price',ascending=False).head(1)
        minimums = cobradas.sort_values(by='price',ascending=False).tail(1)
        total_cobrado = cobradas.price.sum()
        total_nocobrado = no_cobradas.price.sum()

        rechazos = transactions.groupby(['Name','payment']).agg({'payment': 'count'}).rename(columns={'payment':'COUNT'})
        rechazos = rechazos.reset_index(level=[0,1])
        mas_rechazado = rechazos[rechazos['payment'] == False].sort_values(by='COUNT',ascending=False).head(1)

        return Response({'Resumen':{
                            'Empresa con mas ventas':maximums,
                            'Empresa con menos ventas':minimums,
                            'Total de transacciones cobradas' : total_cobrado,
                            'Total de transacciones no cobradas' : total_nocobrado,
                            'Empresa mas rechazada': mas_rechazado}
        })

class Detail(APIView):
    def get(self, request,name, format=None):
        try:
            company_query = models.company.objects.get(name=name)
        except models.company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # print(company_query.id)
        query = str(company_query.id)
        try:
            transactions_query = transaction.objects.filter(id_company=query)
            # query_transactions_json = parser.serialize('json', transactions_query)

            # query_transactions_json = json.loads(query_transactions_json)

            # transactions_query = [{'pk':transaction['pk'], 'data':transaction['fields']} for transaction in query_transactions_json if str(transaction['fields']['id_company']) == query]
            cobradas = [transaction for transaction in transactions_query if transaction.final_charge == True]
            no_cobradas = [transaction for transaction in transactions_query if transaction.final_charge == False]
            fechas = [[str(transaction.date_transaction.day),str(transaction.date_transaction.month),str(transaction.date_transaction.year)] for transaction in transactions_query]

        except transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        fechas = pd.Series(fechas)

        # print(fechas)
        mas_transacciones = fechas.value_counts().head(1).reset_index()
        # print(mas_transacciones['index'][0])
        # print(sum(cobradas))
        # print(transactions_query[0].status)
        print(mas_transacciones)

        return Response({'Data': {
                            'Nombre':company_query.name,
                            'Total cobradas':{
                                'Cantidad':len(cobradas),
                                'Monto' : sum(tran.price for tran in cobradas)
                            },
                            'Total no cobradas':{
                                'Cantidad':len(no_cobradas),
                                'Monto':sum(tran.price for tran in no_cobradas)
                            },
                            'Dia con mas transacciones' : '/'.join(mas_transacciones['index'][0])
        }})
