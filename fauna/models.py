from django.db import models


# Create your models here.

class Animal(models.Model):
    class Meta:
        ordering = ['name']

    PERIOD_CHOICES = [
        ("PERMIAN", 'Permian'),
        ("TRIASSIC", 'Triassic'),
        ("JURASSIC", 'Jurassic'),
        ("CRETACEOUS", 'Cretaceous'),
        ("PALEOGENE", 'Paleogene'),
        ("NEOGENE", 'Neogene'),
        ("QUATERNARY", 'Quaternary'),
    ]

    name = models.CharField(max_length=50, blank=False, null=False)
    extinction = models.CharField(max_length=50, blank=False, null=False)
    period = models.CharField(max_length=50, blank=False, null=False, choices=PERIOD_CHOICES)
    taxonomy_class = models.CharField(max_length=50, blank=False, null=False)
    taxonomy_order = models.CharField(max_length=50, blank=False, null=False)
    taxonomy_family = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.name} of {self.taxonomy_family}"

