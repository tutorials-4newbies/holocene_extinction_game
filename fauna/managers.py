from django.db import models
from django.db.models import Q


class AnimalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(is_deactivated=False) | Q(its_alive=True))

    def with_likes(self):
        return self.prefetch_related("likes").annotate(count=models.Count("likes"))