from django.db.models import Avg
from django.forms import ValidationError
from rest_framework import serializers
from reviews.models import Categories, Comment, Genres, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genres


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Categories


class TitlePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genres.objects,
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categories.objects
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField("get_rating")

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
            "rating",
        )
        model = Title

    def get_rating(self, title):
        reviews = Review.objects.filter(title=title)
        rating = reviews.all().aggregate(Avg("score"))
        result = rating["score__avg"]
        return result


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username")
    review = serializers.SlugRelatedField(
        read_only=True, slug_field="id")

    class Meta:
        model = Comment
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field="id",
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        title = self.context["view"].kwargs["title_id"]
        author = self.context["request"].user
        is_exists = Review.objects.filter(title=title, author=author)
        if self.context["request"].method != "PATCH":
            if is_exists:
                raise ValidationError(
                    "Вы уже оставляли ревью к этому произведению")
        return data

    class Meta:
        model = Review
        fields = "__all__"
