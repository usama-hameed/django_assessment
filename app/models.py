from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import date
# Create your models here.


class Movies(models.Model):
    name = models.CharField(max_length=225, null=False, blank=False)
    protagonists = ArrayField(models.CharField(max_length=225, null=False, blank=False))
    poster = models.ImageField(upload_to='poster', null=False, blank=False)
    start_date = models.DateField(default=date.today)
    status = models.CharField(max_length=50, default='upcoming')
    ranking = models.IntegerField(default=0)

    def __str__(self):
        return self.name
