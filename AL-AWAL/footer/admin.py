"""
Configure the administrator MyInformation.
"""

from django.contrib import admin

from . import models


@admin.register(models.MyInformation)
class FooterAdmin(admin.ModelAdmin):
    """display Model of MyInformation with some modifications to its functionality."""

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if models.MyInformation.objects.count() > 0:
            return False
        return super().has_add_permission(request)
