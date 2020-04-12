from django.contrib import messages
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from rest_framework import serializers
from rest_framework import viewsets

from .models import Store, Review, VisitorCity, DefaultFont
from .utils import lat_lng_to_city


#@cache_page(60 * 60)
def all_stores(request, lat, lng):
    city = lat_lng_to_city(lat, lng)
    point = Point(float(lng), float(lat), srid=4326)
    nearest_stores = Store.objects.filter(city__name_in_google=city).annotate(
        distance=Distance("distance_point", point)
    ).order_by("distance")

    if nearest_stores.count() == 0:
        try:
            v_city = VisitorCity.objects.get(name=city)
            v_city.visitors += 1
            v_city.save()
        except VisitorCity.DoesNotExist:
            VisitorCity.objects.create(name=city, visitors=1)

        messages.add_message(request, messages.ERROR, _("There is no store nearby."))
        return redirect("location-input")

    default_font_settings = DefaultFont.objects.get(key="ALL_STORE")

    return render(
        request,
        "store/all-stores-2.html",
        {
            "lat": lat,
            "lng": lng,
            "nearest_stores": nearest_stores,
            "city": nearest_stores[0].city,
            "default_font_settings": default_font_settings,
        },
    )


@cache_page(60 * 60)
def store_profile(request, store_id, lat=None, lng=None):
    store = get_object_or_404(Store, id=store_id)
    review_list = Review.objects.filter(store=store, approved=True)
    paginator = Paginator(review_list, 5)  # Show 5 contacts per page
    page = request.GET.get("page", 1)
    try:
        reviews = paginator.get_page(page)
    except EmptyPage:
        reviews = paginator.get_page(paginator.num_pages)

    return render(
        request,
        "store/profile.html",
        {
            "store": store,
            "lat": lat,
            "lng": lng,
            "reviews": reviews,
            "empty": True if review_list.count() is 0 else False,
        },
    )

@cache_page(60 * 60)
def direction(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    return render(request, "store/direction.html", {"store": store})


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ("id", "approved")


class ReviewViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    serializer_class = ReviewSerializer
    queryset = Review.objects.filter(approved=True)


def more_reviews(request, store_id, page_id):
    review_list = Review.objects.filter(store__id=store_id, approved=True)
    paginator = Paginator(review_list, 5)  # Show 5 contacts per page
    if paginator.num_pages < page_id:
        raise Http404
    reviews = paginator.get_page(page_id)

    return render(request, "store/review.html", {"reviews": reviews})
