"""Urls definition"""

from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", views.about_us, name="aboutus"),
    path("publishers/", views.publisher, name="publishers"),
    path("specialeducation/", views.specialeducation, name="specialeducation"),
    path("contact-us/", views.contact_us, name="contactus"),
    path("sign-up-and-log-in/", views.sign_up, name="sign-up-and-log-in"),
    path("addbook/<int:id_>/", views.add_to_cart, name="addbook"),
    path("removebook/<int:id_>", views.removefromcart, name="removebook"),
    path(
        "incrementbook/<int:id_>", views.incrementcart, name="incrementbooks"
    ),
    path(
        "decrementbook/<int:id_>", views.decrementcart, name="decrementbooks"
    ),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("forget-password/", views.forgetpass, name="forget-password"),
    path(
        "set-new-password/<uidb64>/<token>",
        views.complete_password_reset,
        name="set-new-password",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("payment/", views.payment, name="payment"),
]
