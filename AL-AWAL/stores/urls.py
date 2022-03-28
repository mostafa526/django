"""Urls definition"""

from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("booksforsale/", views.booksforsale, name="booksforsale"),
    path(
        "booksforsale/<str:slug>",
        views.booksforsale_subcategory,
        name="booksforsale_subcategory",
    ),
]
