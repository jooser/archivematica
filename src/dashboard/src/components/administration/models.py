from django.db import models
from main.models import UUIDPkField

class ReplacementDict(models.Model):
    id = UUIDPkField()
    dictname = models.CharField(max_length=50)
    position = models.IntegerField(default=1)
    parameter = models.CharField(max_length=50)
    displayname = models.CharField(max_length=50)
    displayvalue = models.CharField(max_lenght=50)
    hidden = models.IntegerField()

    class Meta:
        db_table = u'ReplacementDict'