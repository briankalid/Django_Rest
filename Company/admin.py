from django.contrib import admin

# Register your models here.
from .models import company



@admin.register(company)
class company_admin(admin.ModelAdmin):
    """company 	price 	date 	status_transaction 	status_approved"""
    list_display = ['company','price','date','status_transaction','status_approved']
