from rest_framework import serializers


def validate_passwords(password, password_confirmation):
    if password != password_confirmation:
        raise serializers.ValidationError("Passwords do not match.")

