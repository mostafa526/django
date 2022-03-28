"""Urls definition"""

from django.urls import path

from . import views

app_name = "book"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path(
        "bookforsale/<str:slug>/<slug:slug_book>",
        views.book_detail,
        name="detail",
    ),
]
