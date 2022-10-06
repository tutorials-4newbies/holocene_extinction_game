from rest_framework import serializers

from fauna.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"


# Add an anonymous user serialzier with a limited list of fields
