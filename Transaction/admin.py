from django.contrib import admin

# Register your models here.
from .models import transaction

@admin.register(transaction)
class transaction_admin(admin.ModelAdmin):
    list_display = ['id','price','date_transaction','final_charge']
