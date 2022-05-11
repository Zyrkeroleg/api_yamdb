from rest_framework import serializers

from reviews.models import Genres, Categories, Titles


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class TitleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Titles
