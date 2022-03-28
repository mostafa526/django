"""
Configure the model MyInformation.
"""

from django.db import models


class MyInformationManager(models.Manager):
    def first_row(self):
        return self.filter(id=1).first()


class MyInformation(models.Model):
    """Model definition for MyInformation."""

    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=100)
    facebook_link = models.URLField(null=True, blank=True)
    instgram_link = models.URLField(null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    objects = MyInformationManager()

    class Meta:
        verbose_name_plural = "company contacts"

    def __str__(self):
        return "company contacts"
