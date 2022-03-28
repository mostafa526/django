"""
Configure the administrator for both Order and Book.
"""

from django.contrib import admin

from . import models

admin.site.site_title = "FIRST LTD"
admin.site.site_header = "FIRST LTD"


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """display Model of Order with some modifications to its functionality."""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    """display Model of Book with some modifications to its functionality."""

    readonly_fields = ("slug_book",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["subcategory"].widget.can_add_related = False
        form.base_fields["subcategory"].widget.can_change_related = False
        return form
