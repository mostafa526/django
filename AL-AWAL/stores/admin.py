"""
Configure the administrator Category and Subcategory.
"""

from django.contrib import admin

from . import models


@admin.register(models.Category)
class Admin(admin.ModelAdmin):
    """display Model of Category with some modifications to its functionality."""

    readonly_fields = ("slug",)


admin.site.register(models.Subcategory)
