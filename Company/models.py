import uuid
from django.db import models

# Create your models here.
class company(models.Model):
    name = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=10, default='activa')
    id =  models.CharField(max_length=100,primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    # id =  models.CharField(max_length=32,primary_key=True, default=str(uuid.uuid4), editable=False)

    def __str__(self):
        return str(self.id)
