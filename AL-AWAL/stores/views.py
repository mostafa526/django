"""
Define views and constraints for each view.
"""

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


def booksforsale(request):
    """Define the Book For Sale display function."""

    context = footer_and_category()

    return render(request, "booksforsale.html", context)


def booksforsale_subcategory(request, slug):
    """Define the Book For Sale To Subcategory display function."""

    specific_category = Category.objects.filter(slug=slug).first()
    subcategory = specific_category.subcategory.all()
    book = Book.objects.filter(category=specific_category.id)

    subcategory_list = []
    for _ in subcategory:
        for single_book in book:
            if single_book.subcategory is None:
                continue
            if single_book.subcategory.name not in subcategory_list:
                subcategory_list.append(single_book.subcategory.name)

    subcategory_list = set(subcategory_list)
    subcategory_list = list(subcategory_list)

    subcategory = specific_category.subcategory.filter(
        name__in=subcategory_list
    )

    context = footer_and_category()
    context.update(
        {
            "specific_category": specific_category,
            "subcategory": subcategory,
            "book": book,
        }
    )

    return render(request, "onecategorybookswithcategories.html", context)
