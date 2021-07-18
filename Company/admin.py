from django.contrib import admin

# Register your models here.
from .models import company



@admin.register(company)
class company_admin(admin.ModelAdmin):

    list_display = ['name','status','id']
