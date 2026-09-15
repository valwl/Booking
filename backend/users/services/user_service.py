from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:
    @classmethod
    def change_user_password(cls, user, new_password) -> None:
        user.set_password(new_password)
        user.save(update_fields=["password"])

    @staticmethod
    def update_profile(user, **fields):
        for attr, value in fields.items():
            setattr(user, attr, value)
        user.save()
        return user
