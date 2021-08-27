from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class CustomAccountManager(BaseUserManager):

    def createUser(self, email, username, password, first_name, token):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, token=token)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password, **otherfields):
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_superuser', True)
        otherfields.setdefault('is_active', True)
        if otherfields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if otherfields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        email = self.normalize_email(email)
        super_user = self.model(email=email, password=password, username=username, **otherfields)
        super_user.set_password(password)
        super_user.save()

        return super_user


class ExUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=192, unique=True)
    password = models.CharField(max_length=192)
    first_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True)
    token = models.CharField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = CustomAccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]


class Tokens(models.Model):
    token = models.ForeignKey(ExUser, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


class PC(models.Model):
    name = models.CharField(max_length=192)
    user = models.ForeignKey(ExUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
