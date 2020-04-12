from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    PhotoGallery,
    Store,
    City,
    Review,
    Config,
    DefaultImage,
    DefaultFont,
)

admin.site.register(DefaultFont)


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                u' <a href="%s" target="_blank">'
                u'<img src="%s" alt="%s" width="150" height="150"  style="object-fit: cover;"/></a> %s '
                % (image_url, image_url, file_name, (""))
            )

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u"".join(output))


class BasicTypeAdmin(admin.ModelAdmin):
    list_display = ("id",)


class PhotoGalleryInline(admin.TabularInline):
    model = PhotoGallery
    max_num = 99999999
    formfield_overrides = {models.ImageField: {"widget": AdminImageWidget}}


admin.site.register(PhotoGallery, BasicTypeAdmin)

class StoreResource(resources.ModelResource):
    class Meta:
        model = Store
        exclude = [
            "distance_point",
            "cover_photo",
        ]


class StoreAdmin(ImportExportModelAdmin):
    resource_class = StoreResource
    list_display = ("id", "phone_number", "city", "address_in_bn", "address_in_en")
    search_fields = ("phone_number", "address_in_bn", "address_in_en")
    inlines = [PhotoGalleryInline]
    list_filter = ("city",)


admin.site.register(Store, StoreAdmin)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "name_in_bn", "name_in_google", "created_at")
    date_hierarchy = "created_at"
    search_fields = ("name", "name_in_bn", "name_in_google")
    readonly_fields = ("name_in_google",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rating", "store", "approved")
    list_filter = ("approved", "rating")
    search_fields = ("name", "store")


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "value")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(DefaultImage)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "value")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
