from django.db import models


class AnimalStats(models.Model):
    animal = models.OneToOneField(to="fauna.Animal", on_delete=models.CASCADE)
    is_loved = models.BooleanField(default=False)