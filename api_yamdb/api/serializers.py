from rest_framework import serializers

from reviews.models import Genres, Categories, Titles


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Categories


class TitleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = GenreSerializer
    category = CategorySerializer
    """genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects,
        many=True,
    )"""

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Titles
