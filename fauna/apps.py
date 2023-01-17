from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


def setup_profile(sender, instance, created, *args, **kwargs):
    from fauna.models import Profile
    Profile.create_profile(user=instance)


class FaunaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fauna'

    def ready(self):
        post_save.connect(receiver=setup_profile, sender=get_user_model())
