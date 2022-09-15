from django.db import models


# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="שם")
    extinction = models.CharField(max_length=50, blank=False, null=False)
    period = models.CharField(max_length=50, blank=False, null=False)
    taxonomy_class = models.CharField(max_length=50, blank=False, null=False)
    taxonomy_order = models.CharField(max_length=50, blank=False, null=False)
    taxonomy_family = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.name} from the {self.period}"
