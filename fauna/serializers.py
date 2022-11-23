from django.contrib.auth import get_user_model
from rest_framework import serializers

from fauna.models import Animal


class AnonymousUserAnimalSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(method_name="get_is_liked")

    class Meta:
        model = Animal
        fields = ["id", "name", "period", "likes_count", "is_liked"]

    def get_is_liked(self, obj: Animal):
        # if the user is anonmyous then no
        request_user = self.context["request"].user
        if not request_user.is_authenticated:
            return False
        return obj.likes.filter(id=request_user.id).exists()


class AnimalSerializer(AnonymousUserAnimalSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Animal
        fields = ["id", "name", "period", "extinction", "taxonomy_class", "taxonomy_order", "taxonomy_family",
                  "creator", "likes_count", "is_liked"]
