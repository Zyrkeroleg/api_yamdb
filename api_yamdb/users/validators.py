from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def email_validator(email):
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError({"email": "Введите корректный email."})
