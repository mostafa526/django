"""
Configure the model MyUser.
"""

from django.conf import settings
from django.db import models


class MyUser(models.Model):
    """Model definition for MyUser."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.user.first_name)
