from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.

class UserProfileManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None) -> "User":
        if not email:
            raise ValueError('Invalid Email')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Custom User Model"""
    first_name = models.CharField(_("first name"), max_length=30, blank=True, default="First Name")
    last_name = models.CharField(_("Last name"), max_length=30, blank=True, default="Last Name")
    email = models.EmailField(_("Email ID"), blank=True, default="Email ID")
    # password = models.CharField(_("Password"), max_length=40, blank=True, default="Password")

    objects = UserProfileManager()

    def __str__(self) -> str:
        return self.first_name

    def __str__(self) -> str:
        return self.email
