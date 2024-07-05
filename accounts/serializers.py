from rest_framework import serializers
from .models import CustomUser

class ParentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class KidLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'personal_id')
        extra_kwargs = {'password': {'write_only': True}}

class KidSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'personal_id')
        extra_kwargs = {'password': {'write_only': True}}

class ParentWithKidsSerializer(serializers.ModelSerializer):
    kids = KidSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'personal_id', 'kids')
