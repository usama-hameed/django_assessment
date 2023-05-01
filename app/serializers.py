from rest_framework import serializers
from .models import Movies


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'

    def update(self, instance, validated_data):
        image = validated_data.pop('poster', None)
        if image:
            instance.poster.delete(save=False)  # Delete the old image file
            instance.poster = image
        return super().update(instance, validated_data)
