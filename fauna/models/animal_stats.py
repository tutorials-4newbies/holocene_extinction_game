from django.db import models
from django.db.models import CASCADE


class AnimalStats(models.Model):
    animal = models.OneToOneField(to="fauna.Animal", on_delete=CASCADE, related_name="stats")
    is_loved = models.BooleanField(default=True)
    high_fives = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"stats for {self.animal}"
