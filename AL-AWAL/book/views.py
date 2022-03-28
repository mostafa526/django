"""
Define views and constraints for each view.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from book.models import Book
from footer.models import MyInformation
from stores.models import Category


def footer_and_category():
    """define a function to get footer and categories."""

    footer = MyInformation.objects.first_row()
    category = Category.objects.all()
    book_list = []
    for single_category in category:
        if not Book.objects.filter(
            category__name=single_category.name
        ).exists():
            book_list.append(single_category.name)
    category = Category.objects.exclude(name__in=book_list)
    context = {
        "footer": footer,
        "category": category,
    }
    return context


@login_required(login_url="/sign-up-and-log-in/")
def checkout(request):
    """Define the Checkout display function."""

    books = request.session.get("menu", [])
    context = footer_and_category()

    book_id_list = []
    if "menu" in request.session:
        context["books"] = books
        for single_book in context["books"]:
            book_id_list.append(single_book["id"])
            book_session = Book.objects.filter(id=single_book["id"]).first()
            single_book["name"] = book_session.name
            single_book["price"] = book_session.price
            single_book["image"] = book_session.image_url
            single_book["description"] = book_session.description

    return render(request, "checkout.html", context)


def book_detail(request, slug, slug_book):
    """Define the Book Detail display function."""

    specific_category = Category.objects.filter(slug=slug).first()
    similar = Book.objects.filter(category=specific_category)
    single_book = Book.objects.filter(slug_book=slug_book).first()
    context = footer_and_category()
    context.update(
        {
            "specific_category": specific_category,
            "single_book": single_book,
            "book_similar": similar,
        }
    )

    return render(request, "bookDetailsPage.html", context)
