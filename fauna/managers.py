from django.db import models
from django.db.models import Q, F


class AnimalFullManager(models.Manager):

    def with_counts(self):
        return self.annotate(count=models.Count("likes"))


class AnimalManager(AnimalFullManager):

    def get_queryset(self):
        return super().get_queryset().filter(Q(is_deactivated=False) | Q(its_alive=True))
