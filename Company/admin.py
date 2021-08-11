from django.contrib import admin

# Register your models here.
from .models import company

import pandas

@admin.register(company)
class company_admin(admin.ModelAdmin):

    list_display = ['name','status','id']
