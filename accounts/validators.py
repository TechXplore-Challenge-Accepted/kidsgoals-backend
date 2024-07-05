from django.core.exceptions import ValidationError


def validate_personal_id(value):
    if len(value) != 11:
        raise ValidationError('ID must be exactly 11 characters long')
