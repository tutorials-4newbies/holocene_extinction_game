from django.db import models
from django.conf import settings
from django.db.models import CASCADE


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="profile")
    is_corp_worker = models.BooleanField(default=False)
    is_grandmaster = models.BooleanField(default=False)

    @classmethod
    def create_profile(cls, user: object) -> object:
        profile = Profile.objects.create(user=user)
        return profile
