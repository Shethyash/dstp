from datetime import datetime
from django.db import models

# Create your models here.


class Nodes(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    description = models.TextField(default='')
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)


class Feeds(models.Model):
    c_id = models.IntegerField()
    entry_id = models.IntegerField()
    field1 = models.FloatField(null=True)
    field2 = models.FloatField(null=True)
    field3 = models.FloatField(null=True)
    field4 = models.FloatField(null=True)
    field5 = models.FloatField(null=True)
    field6 = models.FloatField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
