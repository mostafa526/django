"""
Configure the model for both Order, DiscountForBook, and Book.
"""

from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify
from smart_selects.db_fields import ChainedForeignKey

from stores.models import Category, Subcategory
from users.models import MyUser


def rename_image(instance, filename):
    """this function rename image before saving."""

    extension = filename.split(".")[-1]
    image_name = "book-images/{}.{}".format(
        instance.name + "-" + str(instance.id), extension
    )
    return image_name


class Book(models.Model):
    """Model definition for Book."""

    name = models.CharField(max_length=300, null=True)
    price = models.FloatField(null=True)
    code = models.IntegerField(null=True, unique=True)
    image = models.ImageField(upload_to=rename_image, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True, max_length=400)
    subcategory = ChainedForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        chained_field="category",
        chained_model_field="category",
    )
    slug_book = models.SlugField(blank=True, null=True)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.slug_book = (
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

    @property
    def image_url(self):
        """this function check if it image is none or not."""

        url = self.image.url
        if url is None:
            url = ""
        return url


class DiscountForBook(models.Model):
    """Model definition for DiscountForBook."""

    discountrate = models.FloatField(null=True, blank=True)
    discountforbook = models.ForeignKey(
        Book, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return str(self.discountforbook.name)


class Order(models.Model):
    """Model definition for Order."""

    totalprice = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    Book = models.ManyToManyField(Book, blank=True)
    discountbookfororder = models.ForeignKey(
        DiscountForBook, blank=True, on_delete=models.CASCADE, null=True
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user.user.first_name)
