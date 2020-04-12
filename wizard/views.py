from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page


def location_permission(request):
    if request.method == "GET":
        return render(request, "wizard/location-permission.html", {})


def index(request):
    return render(request, "index.html", {})


def we_come_to_you(request):
    return render(request, "wizard/we-come-to-you.html", {})


def location_input(request):
    return render(request, "wizard/location-input.html", {})


def set_language_to_bn(request):
    language = request.session.get("_language", None)
    if language is None:
        return redirect("/bn/")
    else:
        return redirect(f"/{language}/")
