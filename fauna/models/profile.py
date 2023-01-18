from django.db import models
from django.conf import settings
from django.db.models import CASCADE


class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="profile")
    is_verified = models.BooleanField(default=False)
    is_grand_master = models.BooleanField(default=False)

    def __str__(self):
        return f"profile {self.user.username}"

    @classmethod
    def create_profile(cls, user):
        return Profile.objects.create(user=user)
