from django.contrib.auth import get_user_model
from .models import ExUser
from django.contrib.auth.backends import ModelBackend


class CustomBackendModel(ModelBackend):
    def authenticate(self, request, username=None, password=None, token=None, **kwargs):
        try:
            user = ExUser.objects.get(email=username)
        except ExUser.MultipleObjectsReturned:
            user = ExUser.objects.filter(email=username).order_by('id').first()
        except ExUser.DoesNotExist:
            return None
        if getattr(user, 'is_active') and user.check_password(password) and token == user.token:
            return user
        return None

    def get_user(self, id):
        try:
            return ExUser.objects.get(pk=id)
        except:
            return None
