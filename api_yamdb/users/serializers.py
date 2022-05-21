from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class UserSerializerOrReadOnly(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"
        model = User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError("Нельзя подписаться на себя!")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User
        lookup_field = "username"
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email",),
                message="Почта уже существует",
            )
        ]


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
