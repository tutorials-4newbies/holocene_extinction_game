from django.contrib.auth import get_user_model
from rest_framework import serializers

from fauna.models import Animal


class AnonymousUserAnimalSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(method_name="get_is_liked")

    class Meta:
        model = Animal
        fields = ["id", "name", "period", "likes_count", "is_liked", "picture"]

    def get_is_liked(self, obj: Animal):
        # if the user is anonmyous then no
        request_user = self.context["request"].user
        if not request_user.is_authenticated:
            return False
        return obj.likes.filter(id=request_user.id).exists()


class ThinAnimalSerializer(AnonymousUserAnimalSerializer):
    class Meta:
        model = Animal
        fields = ["id", "name"]


class AnimalSerializer(AnonymousUserAnimalSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Animal
        fields = ["id", "name", "period", "extinction", "taxonomy_class", "taxonomy_order", "taxonomy_family",
                  "creator", "likes_count", "is_liked", "picture"]


class AnimalDashBoardSerializer(serializers.Serializer):
    animals_count = serializers.IntegerField(required=False)
    avg_name_length = serializers.IntegerField(required=False)
    longest_name = serializers.CharField(required=False)
    shortest_name = serializers.CharField(required=False)
    most_liked_animal_name = serializers.CharField(required=False)
    top_3_liked_animals = AnimalSerializer(many=True, required=False)


class UsersViewSerializer(serializers.ModelSerializer):
    animals_created = AnimalSerializer(many=True)
    animals_liked = ThinAnimalSerializer(many=True)
    how_many_liked = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "animals_created", "animals_liked", "how_many_liked"]

    def get_how_many_liked(self, obj):
        return obj.animals_liked.count()


class ThinUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class AnimalUserSerializer(serializers.ModelSerializer):
    creator = ThinUserSerializer(many=False, read_only=True)

    class Meta:
        model = Animal
        fields = ["id", "name", "creator"]

