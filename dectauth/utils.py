from django.contrib.auth.models import User
from django.contrib.auth import login


def create_user_and_login(request, challenge):
    user, created = User.objects.get_or_create(
        username=challenge.username,
        email='',
        defaults={}
    )
    user.set_unusable_password()
    user.save()
    login(request, user)
    return user
