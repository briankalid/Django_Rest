import uuid
from django.db import models
from Company.models import company


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# def validate_final_charge()
# Create your models here.
class transaction(models.Model):
    id =  models.CharField(max_length=33,primary_key=True, default=uuid.uuid4, editable=False,unique=True)
    id_company = models.ForeignKey(company,on_delete=models.CASCADE)
    price = models.FloatField()
    date_transaction = models.DateTimeField()
    status_transaction = models.CharField(max_length=20)
    status_approved = models.BooleanField()
    # final_charge = models.BooleanField(default = set_final_charge,editable=False)

    @property
    def final_charge(self):
        return (self.status_transaction=='closed') and (self.status_approved)

    def __str__(self):
        return str(self.id_company)
    # final_charge = property(set_final_charge)
