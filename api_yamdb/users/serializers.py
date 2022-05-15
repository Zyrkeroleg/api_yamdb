from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User

class UserSerializerOrReadOnly(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'
        model = User


class MailSerializer(serializers.Serializer):
    """Сериализатор для mail"""
    email = serializers.EmailField(required=True)
