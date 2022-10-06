from rest_framework import serializers

from fauna.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ["name", "period", "extinction", "taxonomy_class", "taxonomy_order", "taxonomy_family"]



class AnonymousUserAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ["name", "period"]
