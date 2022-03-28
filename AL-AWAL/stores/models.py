"""
Configure the model for both Subcategory, and Category.
"""

from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify


class Subcategory(models.Model):
    """Model definition for Subcategory."""

    name = models.CharField(max_length=300, null=True, unique=True)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    """Model definition for Category."""

    name = models.CharField(max_length=300, unique=True)
    subcategory = models.ManyToManyField(Subcategory, blank=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.slug = (
            slugify(self.name)
            + "-"
            + str(urlsafe_base64_encode(force_bytes(self.pk)))
        )
        super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    def __str__(self):
        return str(self.name)
