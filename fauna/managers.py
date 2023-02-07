from django.db import models


class AnimalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deactivated=False)

    def with_likes(self):
        return self.annotate(count=models.Count("likes"))