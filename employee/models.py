import binascii
import os

from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}token={}".format(reverse('password_reset:reset-password-request'),
                                                  reset_password_token.key)
    send_mail(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        "noreply@somehost.local",
        [reset_password_token.user.email]
    )


class DBOTRequest(models.Model):
    employee = models.CharField(default=None, max_length=100, null=True)
    manager = models.CharField(default=None, max_length=100)
    title = models.CharField(default=None, max_length=100)
    description = models.TextField(default=None, )
    date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(default=None, )
    end_time = models.DateTimeField(default=None, )
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = "DBOTRequest"


class UserS(AbstractBaseUser):
    username = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=128, default=None)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=255, unique=True)
    department = models.CharField(max_length=255, default=None)

    object = UserManager()

    class Meta:
        db_table = "Employee"
        indexes = [
            models.Index(fields=["email"], name="email_index"),
        ]

    def __str__(self):
        return self.email


