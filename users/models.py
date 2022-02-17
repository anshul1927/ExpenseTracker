from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
# Create your models here.


class User(models.Model):
    """Custom User Model"""
    first_name = models.CharField(_("first name"), max_length=30, blank=True, default="First Name")
    last_name = models.CharField(_("Last name"), max_length=30, blank=True, default="Last Name")
    email = models.EmailField(_("Email ID"), blank=True, default="Email ID")
    password = models.CharField(_("Password"),max_length=40, blank=True, default="Password")

    def __str__(self)-> str:
        return self.first_name