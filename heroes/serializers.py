from rest_framework import serializers

from .models import HeroModel


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroModel
        fields = ["name", "description", "city"]
