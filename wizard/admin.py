from django.contrib import admin

from .models import EnglishFont, BanglaFont


class FontAdmin(admin.ModelAdmin):
    list_display = ("font_family", "font_file", "language", "created_at")
    date_hierarchy = "created_at"
    search_fields = ("font_family",)
    list_filter = ("language",)


admin.site.register(EnglishFont)
admin.site.register(BanglaFont)
