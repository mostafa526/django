"""
Configure the model Publishers.
"""

from django.db import models


def rename_image(instance, filename):
    """this function rename image before saving."""

    extension = filename.split(".")[-1]
    image_name = "publisher-images/{}.{}".format(
        instance.nameofsupplier + "-" + str(instance.id), extension
    )
    return image_name


class Publishers(models.Model):
    """Model definition for Publishers."""

    nameofsupplier = models.CharField(max_length=300, null=True)
    logo = models.ImageField(upload_to=rename_image, null=True)
    moreinformation = models.TextField(null=True)
    websitelink = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Publishers"

    def __str__(self):
        return str(self.nameofsupplier)

    @property
    def image_url(self):
        """this function check if it image is none or not."""

        url = self.logo.url
        if url is None:
            url = ""
        return url
