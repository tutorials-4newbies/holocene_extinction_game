from django.contrib.auth import get_user_model
from rest_framework import serializers

from fauna.models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Animal
        fields = ["id", "name", "period", "extinction", "taxonomy_class", "taxonomy_order", "taxonomy_family",
                  "creator"]


class AnonymousUserAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ["id", "name", "period"]
