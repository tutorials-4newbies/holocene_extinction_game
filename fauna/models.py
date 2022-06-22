from django.db import models


# Create your models here.

class Animal(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False)
    extinction = models.CharField(max_length=50, blank=False, null=False)
    period = models.CharField(max_length=50, blank=False, null=False)
    animal_class = models.CharField(max_length=50, blank=False, null=False)
    order = models.CharField(max_length=50, blank=False, null=False)
    family = models.CharField(max_length=50, blank=False, null=False)

