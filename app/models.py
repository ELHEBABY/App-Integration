from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.

class IntegrationSettings(models.Model):
    integration_automatic_is_active = models.BooleanField("Integration automatic",default=False)

    frequency=(
        ('day','day'),
        ('two_day','two_day'),
        ('week','week'))
    integration_frequency = models.CharField( max_length=50, choices=frequency, default='day')
