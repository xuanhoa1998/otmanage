from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        "noreply@somehost.local",
        [reset_password_token.user.email]
    )


class DBOTRequest(models.Model):
    employee = models.CharField(default=None, max_length=100)
    manager = models.CharField(default=None, max_length=100)
    title = models.CharField(default=None, max_length=100)
    description = models.TextField(default=None, )
    date = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(default=None, )
    end_time = models.DateTimeField(default=None, )
    approved = models.BooleanField(default=False)
    class Meta:
        db_table = "DBOTRequest"