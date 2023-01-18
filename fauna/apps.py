from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


def create_profile(sender, instance, created, *args, **kwargs):
    """
    created - a boolean
    sender - the CLASS calling
    instance - the class instance
    """
    from fauna.models import Profile

    if created:
        Profile.create_profile(user=instance)


class FaunaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fauna'

    def ready(self):
        post_save.connect(receiver=create_profile, sender=get_user_model())
