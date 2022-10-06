from rest_framework import serializers

from fauna.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"


class AnonymousAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['name', 'period']
