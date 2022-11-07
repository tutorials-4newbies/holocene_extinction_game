from django.contrib.auth import get_user_model
from rest_framework import serializers

from fauna.models import Animal

class AnonymousUserAnimalSerializer(serializers.ModelSerializer):


    class Meta:
        model = Animal
        fields = ["id", "name", "period", "likes_count"]



class AnimalSerializer(AnonymousUserAnimalSerializer):
    is_liked = serializers.BooleanField(read_only=True)
    creator = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Animal
        fields = ["id", "name", "period", "extinction", "taxonomy_class", "taxonomy_order", "taxonomy_family",
                  "creator","likes_count","is_liked"]



