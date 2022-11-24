from django.db import models
from django.conf import settings
from django.db.models import CASCADE


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
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=CASCADE, related_name="animals_created") #ONE TO MANY
    picture = models.FileField(upload_to="fauna/animals/", null=True, blank=True)
    likes = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="animals_liked", null=True, blank=True)

    def __str__(self):
        return f"{self.name} of {self.taxonomy_family}"

    @property
    def likes_count(self) -> int:
        # Optimization issue lurking here... we'll get back to that
        return self.likes.all().count()

