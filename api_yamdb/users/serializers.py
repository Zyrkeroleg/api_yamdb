from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = User