"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from rest_framework import routers

from store.views import (
    all_stores,
    store_profile,
    ReviewViewSet,
    more_reviews,
    direction,
)
from wizard.views import location_permission, location_input, set_language_to_bn, index, we_come_to_you

admin.site.index_title = _("GasFinder")
admin.site.site_header = _("GasFinder Administration")
admin.site.site_title = _("GasFinder Management")

router = routers.DefaultRouter()
router.register(r"reviews", ReviewViewSet)

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", set_language_to_bn, name="set_language_tp_bn"),
    path(
        "flatpage/privacy-policy/",
        TemplateView.as_view(template_name="privacy-policy.html"),
        name="privacy-policy",
    ),
]

urlpatterns = (
    urlpatterns
    + i18n_patterns(
        path("api/", include(router.urls)),
        path("admin/", admin.site.urls),
        path("", index, name="index"),
        path("location-permission", location_permission, name="location-permission"),
        path("location_input/", location_input, name="location-input"),
        path("we-come-to-you/", we_come_to_you, name="we_come_to_you"),
        path("stores-near-you/<str:lat>/<str:lng>/", all_stores, name="all-store"),
        path(
            "store/<int:store_id>/<str:lat>/<str:lng>/",
            store_profile,
            name="store_profile",
        ),
        path("direction/<int:store_id>/", direction, name="direction"),
        path("store/<int:store_id>/", store_profile, name="store_profile"),
        path(
            "more_reviews/<int:store_id>/<int:page_id>/",
            more_reviews,
            name="more_reviews",
        ),
        prefix_default_language=True,
    )
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
