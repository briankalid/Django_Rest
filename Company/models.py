import uuid
from django.db import models

# Create your models here.
class company(models.Model):
    name = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=10, default='activa')
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name
