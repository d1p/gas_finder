from django.db import models


class EnglishFont(models.Model):
    font_file = models.FileField(upload_to="fonts/")
    font_family = models.CharField(max_length=300, unique=True)
    fallback_font_family = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.font_family


class BanglaFont(models.Model):
    font_file = models.FileField(upload_to="fonts/")
    font_family = models.CharField(max_length=300, unique=True)
    fallback_font_family = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.font_family
