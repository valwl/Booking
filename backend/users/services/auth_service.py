from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class AuthService:
    @staticmethod
    def login(credential: str, password: str) -> User:
        user = authenticate(username=credential, password=password)
        if not user:
            raise ValidationError("Invalid credentials")
        return user

    @staticmethod
    def register(email=None, phone_number=None, password=None, first_name=None, last_name=None) -> User:
        if not email and not phone_number:
            raise ValidationError("Email or phone required")
        return User.objects.create_user(
            email=email,
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
