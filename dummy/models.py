from django.db import models

# Create your models here.

class Dummy(models.Model):

    greeting = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
