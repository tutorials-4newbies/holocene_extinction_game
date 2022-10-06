from rest_framework import serializers

from fauna.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = [
            "name",
            "extinction",
            "period",
            "taxonomy_class",
            "taxonomy_order",
            "taxonomy_family"
        ]

class AnonymosUsesrAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ["name", "period"]