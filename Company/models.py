from django.db import models

# Create your models here.
class company(models.Model):
    company = models.CharField(max_length=100)
    price = models.FloatField()
    date = models.DateTimeField()
    status_transaction = models.CharField(max_length=50)
    status_approved = models.BooleanField()

    def __str__(self):
        return self.company
