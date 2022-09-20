from django.db import models


# Create your models here.
from fauna.choices import PERIOD_CHOICES


class Animal(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False, verbose_name="The name she is called")
    extinction = models.CharField(max_length=50, blank=False, null=False)
    period = models.CharField(max_length=50, blank=False, null=False, choices=PERIOD_CHOICES)
    taxonomy_class = models.CharField(max_length=50, blank=False, null=False)
    taxonomy_order = models.CharField(max_length=50, blank=False, null=False)
    taxonomy_family = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.name} of {self.taxonomy_family}"

