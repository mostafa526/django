"""
Define views and constraints for each view.
"""

import threading

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from email_validator import EmailNotValidError, validate_email

from book.models import Book
from footer.models import MyInformation
from publishers.models import Publishers
from stores.models import Category

from .valid import Check


def footer_and_category():
    """define a function to get footer and categories."""

    footer = MyInformation.objects.first_row()

    category = Book.objects.select_related("category").values_list(
        "category__name", flat=True
    )
    category = Category.objects.filter(name__in=category)

    context = {
        "footer": footer,
        "category": category,
    }

    return context


def error_404_view(request, exception):
    context = footer_and_category()
    return render(request, "404.html", context)


class EmailThread(threading.Thread):
    """Send e-mail faster"""

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def home(request):
    """Define the Home display function."""

    publishers = Publishers.objects.all().order_by("-id")[:8]
    context = footer_and_category()
    context.update(
        {
            "publisher": publishers,
        }
    )

    return render(request, "index.html", context)


def about_us(request):
    """Define the About-us display function."""

    context = footer_and_category()

    return render(request, "aboutus.html", context)


def publisher(request):
    """Define the Publisher display function."""

    publishers = Publishers.objects.all()
    context = footer_and_category()
    context.update(
        {
            "publishers": publishers,
        }
    )

    return render(request, "publishers.html", context)


def specialeducation(request):
    """Define the SpecialEduction display function."""

    context = footer_and_category()

    return render(request, "specialeducation.html", context)


def contact_us(request):
    """Define the Contact us display function."""

    context = footer_and_category()

    email = request.POST.get("email")
    name = request.POST.get("name")
    phone = request.POST.get("Phonenumber")
    content = request.POST.get("msg")
    if name is None or phone is None or content is None or email is None:
        pass
    else:
        try:
            is_valid = validate_email(email)
            _ = is_valid.email
            Check.valid_email_contact_us = True
        except EmailNotValidError:
            Check.valid_email_contact_us = False

    if not Check.valid_email_contact_us and request.method == "POST":
        messages.error(request, "The email has not been sent")

    if request.method == "POST" and Check.valid_email_contact_us:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["Phonenumber"]
        content = request.POST["msg"]

        message = name + "\n" + email + "\n" + phone + "\n\n" + content

        email = EmailMessage(
            "Contact-Us",
            message,
            "am8540689@gmail.com",
            ["tefa2436@gmail.com"],
        )
        EmailThread(email).start()
        messages.success(request, "Email sent successfully")

    return render(request, "contactus.html", context)


def sign_up(request):
    """Define the Sign-up display function."""

    context = footer_and_category()
    name = request.POST.get("Username")
    password = request.POST.get("Password")
    email = request.POST.get("Email")

    if "login" in request.POST:
        return log_in(request)

    if (
        request.method == "POST"
        and request.POST.get("next") == "Sign up"
        and Check.valid
        and Check.valid_email
        and Check.valid_password
    ):

        user = get_user_model().objects.create_user(username=name, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        domain = request.get_host()
        # current_site = get_current_site(request).domain
        message = render_to_string(
            "val.html",
            {
                "user": user,
                "domain": domain,
                "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )
        email = EmailMessage(
            "Activate your account",  # subject
            message,  # body
            "am8540689@gmail.com",  # from
            to=[email],  # to
        )
        EmailThread(email).start()
        return render(request, "emailSendConfirmation_signup.html", context)
    elif request.method == "POST" and request.POST.get("next") == "Sign up":
        return HttpResponse(status=204)

    response_data = {}

    try:
        if name is not None:
            if not get_user_model().objects.filter(username=name).exists():
                Check.valid = True
                response_data["is_success"] = True
            else:
                Check.valid = False
                response_data["is_success"] = False

        if email is not None:
            if not get_user_model().objects.filter(email=email).exists():
                Check.valid_email = True
                response_data["is_success_email"] = True

                try:
                    is_valid = validate_email(email)
                    _ = is_valid.email
                    Check.valid_email = True
                except EmailNotValidError:
                    Check.valid_email = False
                    response_data["is_success_email"] = False

            else:
                Check.valid_email = False
                response_data["is_success_email"] = False

        if password is not None:
            if len(password) > 8:
                response_data["is_success_password"] = True
                Check.valid_password = True
            else:
                response_data["is_success_password"] = False
                Check.valid_password = False

    except ObjectDoesNotExist:
        response_data["is_success"] = False
        response_data["is_success_email"] = False
        response_data["is_success_password"] = False
        response_data["msg"] = "Some error occurred. Please let Admin know."
    if name is None and email is None and password is None:
        return render(request, "signupandlogin.html", context)
    return JsonResponse(response_data)


def log_in(request):
    """Define the Log-in display function."""

    context = footer_and_category()
    name = request.POST["Username"]
    password = request.POST["Password"]
    try:
        user = authenticate(username=name, password=password)
        if user is not None:
            if user.is_active:
                if user.is_superuser or user.is_staff:
                    login(
                        request, authenticate(username=name, password=password)
                    )
                    return redirect("/admin/")
                login(request, authenticate(username=name, password=password))
                if Check.next_login is not None:
                    return redirect(Check.next_login)
            return redirect("/")
        messages.error(request, "Username and password did not matched")
        return render(request, "signupandlogin.html", context)
    except ObjectDoesNotExist:
        pass


def activate(request, uidb64, token):
    """Define a function to activate the email."""

    context = footer_and_category()

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.filter(id=uid).first()
    except (
        TypeError,
        ValueError,
        OverflowError,
        get_user_model().DoesNotExist,
    ):
        user = None
    if (
        user is not None
        and default_token_generator.check_token(user, token)
        and not user.is_active
    ):
        user.is_active = True
        user.save()
        return redirect("/")
    return render(request, "youHaveUsedThisLinkBefore.html", context)


menu = []


class MenuItem:  # pylint: disable=too-few-public-methods
    """Define the menu items to cart."""

    def __init__(self, id_):
        self.id = id_
        self.quantity = 1

    def serialize(self):
        """this function to serialize menu item."""
        return self.__dict__


@csrf_exempt
def removefromcart(request, id_):
    """Define a function to remove items from cart."""

    flag = False

    books = request.session["menu"]
    for book in books:
        if book["id"] == id_:
            books.remove(book)
            request.session["menu"] = books

            flag = True

    return HttpResponse(flag)


@csrf_exempt
def incrementcart(request, id_):
    """Define a function to increment items in cart."""

    flag = False
    books = request.session.get("menu", [])
    for book in books:
        if book["id"] == id_:
            book["quantity"] = book["quantity"] + 1
            request.session["menu"] = books
            _ = request.session["menu"]
            flag = True
            return HttpResponse(flag)

    return HttpResponse(flag)


@csrf_exempt
def decrementcart(request, id_):
    """Define a function to decrement items in cart."""

    flag = False
    books = request.session.get("menu", [])
    for book in books:
        if book["id"] == id_:
            if book["quantity"] > 1:
                book["quantity"] = book["quantity"] - 1
            else:
                books.remove(book)
            request.session["menu"] = books
            flag = True

    return HttpResponse(flag)


@login_required(login_url="/sign-up-and-log-in/")
@csrf_exempt
def add_to_cart(request, id_):
    """Define a function to add items to cart."""

    flag = True
    book = MenuItem(id_)
    context = footer_and_category()
    books = request.session.get("menu", [])
    for book in books:
        if book["id"] == id_:
            book["quantity"] = book["quantity"] + 1
            request.session["menu"] = books
            arr = request.session["menu"]
            return HttpResponse(flag)

    object_ser = MenuItem(id_)
    books.append(object_ser.serialize())
    request.session["menu"] = books

    arr = request.session["menu"]
    if request.user.is_authenticated and len(arr) == 1:
        Check.next_cart = False
        context["res"] = HttpResponse(flag)
        return render(request, "booksforsale.html", context)
    return HttpResponse(flag)


def forgetpass(request):
    """Define forget password display function."""

    context = footer_and_category()
    if request.method == "POST":
        email = request.POST["email"]

        try:
            email_pass = validate_email(email)
            _ = email_pass.email
            Check.valid_email_pass = True
        except EmailNotValidError:
            Check.valid_email_pass = False

        if not Check.valid_email_pass:
            messages.error(request, "Please supply a valid email")
        elif not get_user_model().objects.filter(email=email).exists():
            messages.error(request, "This Email does not exists")
        else:
            user = get_user_model().objects.filter(email=email)
            domain = request.get_host()
            message = render_to_string(
                "email_reset.html",
                {
                    "user": user[0],
                    "domain": domain,
                    "uidb64": urlsafe_base64_encode(force_bytes(user[0].pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            email = EmailMessage(
                "Password reset Instructions",  # subject
                message,
                "am8540689@gmail.com",
                to=[email],  # to
            )
            EmailThread(email).start()
            return render(request, "emailSendConfirmation.html", context)

    return render(request, "forgetPassword.html", context)


def complete_password_reset(request, uidb64, token):
    """Define reset password display function."""

    context = footer_and_category()
    context.update(
        {
            "uidb64": uidb64,
            "token": token,
        }
    )

    try:
        user_id = int(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(id=user_id)

        if not default_token_generator.check_token(user, token):
            return render(request, "youHaveUsedThisLinkBefore.html", context)
    except ObjectDoesNotExist:
        pass

    if request.method == "POST":
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            messages.error(request, "Passwords do not match")

        elif len(password1) < 8:
            messages.error(request, "Short Password")
        else:
            try:
                user_id = int(urlsafe_base64_decode(uidb64))
                user = get_user_model().objects.get(id=user_id)
                user.set_password(password1)
                user.save()
                return render(request, "successfulPasswordReset.html", context)
            except ObjectDoesNotExist:
                messages.error(request, "Something went wrong, try again")

    return render(request, "resetnewpassword.html", context)


def logout_view(request):
    """Define log out display function."""

    Check.next_cart = True
    menu.clear()
    if "menu" in request.session:
        del request.session["menu"]
    logout(request)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def payment(request):
    context = footer_and_category()
    book_session = request.session.get("menu", [])
    book_query = Book.objects.all()
    total = 0
    for book_session_one in book_session:
        book_id = book_session_one["id"]
        book_price = book_query.get(id=book_id)
        total += book_price.price * book_session_one["quantity"]
    context.update(
        {
            "subtotal": total,
        }
    )
    return render(request, "payment.html", context)
