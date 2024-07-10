from rest_framework import serializers
from accounts.models import CustomUser
from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer


class RegistrationSerializer(UserCreateSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'password', 'password_confirmation', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        return CustomUser.objects.create_user(**validated_data)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name')


class EmptySerializer(serializers.Serializer):
    pass
