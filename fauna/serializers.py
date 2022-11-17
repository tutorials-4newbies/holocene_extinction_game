from django.contrib.auth import get_user_model
from rest_framework import serializers

from fauna.models import Animal

class AnonymousUserAnimalSerializer(serializers.ModelSerializer):


    class Meta:
        model = Animal
        fields = ["id", "name", "period", "likes_count"]



class AnimalSerializer(AnonymousUserAnimalSerializer):
    is_liked = serializers.SerializerMethodField(method_name='get_is_liked')
    creator = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    def get_is_liked(self, obj):
        request_user = self.context['request'].user
        if request_user.is_anonymous:
            return False
        animal_liked = request_user.animals_liked.filter(id=obj.id).exists()
        return animal_liked


    class Meta:
        model = Animal
        fields = ["id", "name", "period", "extinction", "taxonomy_class", "taxonomy_order", "taxonomy_family",
                  "creator","likes_count","is_liked"]



