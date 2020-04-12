import math
import os
import uuid
from decimal import Decimal

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from wizard.models import EnglishFont, BanglaFont
from .utils import lat_lng_to_city


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)


class City(models.Model):
    FONT_STYLE = (("normal", "Normal"), ("italic", "Italic"), ("oblique", "Oblique"))
    name = models.CharField(max_length=128, unique=True)

    english_font = models.ForeignKey(
        EnglishFont, on_delete=models.SET_NULL, null=True, blank=True
    )
    english_font_size = models.FloatField(null=True, blank=True)
    english_font_weight = models.PositiveSmallIntegerField(null=True, blank=True)
    english_font_style = models.CharField(
        max_length=20, choices=FONT_STYLE, null=True, blank=True
    )
    english_font_color = models.CharField(
        null=True,
        blank=True,
        max_length=6,
        help_text="Color in HEX format. \n " "ex: f1f1f1",
    )
    english_line_height = models.FloatField(
        null=True, blank=True, default=5, help_text="Line Height in REM"
    )
    name_in_bn = models.CharField(max_length=128, unique=True)
    bangla_font = models.ForeignKey(
        BanglaFont, on_delete=models.SET_NULL, null=True, blank=True
    )
    bangla_font_size = models.FloatField(null=True, blank=True)
    bangla_font_weight = models.PositiveSmallIntegerField(null=True, blank=True)
    bangla_font_style = models.CharField(
        max_length=20, choices=FONT_STYLE, null=True, blank=True
    )
    bangla_font_color = models.CharField(
        null=True,
        blank=True,
        max_length=6,
        help_text="Color in HEX format. \n " "ex: f1f1f1",
    )
    bangla_line_height = models.FloatField(
        null=True, blank=True, default=5, help_text="Line Height in REM"
    )
    welcome_message_in_english = models.CharField(max_length=120, null=True, blank=True)
    welcome_message_in_bangla = models.CharField(max_length=120, null=True, blank=True)
    name_in_google = models.CharField(
        max_length=220,
        unique=True,
        null=True,
        blank=True,
        help_text=_("City name from google API."),
    )
    cover_picture = models.ImageField(
        upload_to=RandomFileName("city/cover/"), null=True, blank=True
    )
    lat = models.FloatField()
    lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.name_in_bn}"

    def clean(self):
        try:
            city_name = lat_lng_to_city(self.lat, self.lng)
        except:
            raise ValidationError("Invalid Latitude or Longitude")

        self.name_in_google = city_name

    def get_default_welcome_message_english(self):
        return Config.objects.get(key="DEFAULT_ALL_STORE_WELCOME_ENGLISH").value

    def get_default_welcome_message_bangla(self):
        return Config.objects.get(key="DEFAULT_ALL_STORE_WELCOME_ARABIC").value

    def get_cover_photo(self):
        return DefaultImage.objects.get(key="DEFAULT_CITY_IMAGE").value

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Store(models.Model):
    distributor_name = models.CharField(
        max_length=250, help_text=_("Distributor name " "in English")
    )
    distributor_name_in_bn = models.CharField(
        max_length=250, help_text=_("Distributor name in Bangla")
    )
    cover_photo = models.ImageField(
        upload_to=RandomFileName("store/cover/"), null=True, blank=True
    )
    phone_number = models.CharField(max_length=15)
    address_in_en = models.TextField(
        max_length=1000, verbose_name=_("Address in English")
    )
    address_in_bn = models.TextField(
        max_length=1000, verbose_name=_("Address in Bangla")
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    distance_point = models.PointField(null=True, blank=True, editable=False)

    def clean(self):
        self.distance_point = Point(self.lng, self.lat, srid=4326)

    def photo_gallery(self):
        return PhotoGallery.objects.filter(store=self)

    def get_cover_photo(self):
        return DefaultImage.objects.get(key="DEFAULT_STORE_IMAGE").value

    @property
    def reviews(self):
        return Review.objects.filter(store=self, approved=True).order_by("-created_at")

    @property
    def average_rating(self):
        rating = self.reviews.aggregate(Avg("rating"))
        return (
            math.ceil(rating["rating__avg"]) if rating["rating__avg"] is not None else 0
        )

    @property
    def u_average_rating(self):
        """ Average rating with decimal points """
        rating = self.reviews.aggregate(Avg("rating"))
        return (
            Decimal(rating["rating__avg"]).quantize(Decimal(".1"))
            if rating["rating__avg"] is not None
            else "0.0"
        )


class PhotoGallery(models.Model):
    picture = models.ImageField(upload_to=RandomFileName("store/photo/"))
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, null=True, db_index=True
    )
    name = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(
        null=False, blank=False, validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    comment = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Review on {self.store} by {self.name} at {self.created_at}"


class Config(models.Model):
    key = models.CharField(max_length=120, unique=True, db_index=True)
    value = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = "Default Text"
        verbose_name_plural = "Default Texts"


class DefaultImage(models.Model):
    key = models.CharField(max_length=120, unique=True, db_index=True)
    value = models.ImageField(upload_to=RandomFileName("city/cover/"))

    class Meta:
        verbose_name = "Default Image"
        verbose_name_plural = "Default Images"


class DefaultFont(models.Model):
    FONT_STYLE = (("normal", "Normal"), ("italic", "Italic"), ("oblique", "Oblique"))

    key = models.CharField(max_length=120, unique=True, db_index=True)
    english_font = models.ForeignKey(EnglishFont, on_delete=models.SET_NULL, null=True)
    english_font_size = models.FloatField()
    english_font_weight = models.PositiveSmallIntegerField()
    english_font_style = models.CharField(max_length=20, choices=FONT_STYLE)
    english_font_color = models.CharField(
        max_length=6, help_text="Color in HEX format. \n " "ex: f1f1f1"
    )
    english_line_height = models.FloatField(default=5, help_text="Line Height in REM")

    bangla_font = models.ForeignKey(BanglaFont, on_delete=models.SET_NULL, null=True)
    bangla_font_size = models.FloatField()
    bangla_font_weight = models.PositiveSmallIntegerField()
    bangla_font_style = models.CharField(max_length=20, choices=FONT_STYLE)
    bangla_font_color = models.CharField(
        max_length=6, help_text="Color in HEX format. \n " "ex: f1f1f1"
    )
    bangla_line_height = models.FloatField(default=5, help_text="Line Height in REM")

    class Meta:
        verbose_name = "Default Font"
        verbose_name_plural = "Default Fonts"


class VisitorCity(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    visitors = models.BigIntegerField(default=0)


class RegionCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    name_in_bnabic = models.CharField(max_length=120, unique=True)
    lat = models.CharField(max_length=20)
    long = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Region Category")
        verbose_name_plural = _("Region Categories")
        ordering = ("name", "name_in_bnabic",)


class RegionSubCategory(models.Model):
    parent_category = models.ForeignKey(RegionCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    name_in_bnabic = models.CharField(max_length=120, unique=True)
    lat = models.CharField(max_length=20)
    long = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.parent_category.name}"

    class Meta:
        verbose_name = _("Region Sub Category")
        verbose_name_plural = _("Region Sub Categories")
        ordering = ("name", "name_in_bnabic",)
