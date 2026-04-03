from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

def index(request):
    """Homepage"""
    return render(request, "index.html")

def about(request):
    """About page"""
    return render(request, "about.html")

@require_POST
def toggle_units(request):
    """Toggle between metric and imperial units"""
    current = request.session.get("unit_system", "metric")
    request.session["unit_system"] = "imperial" if current == "metric" else "metric"
    return redirect(request.META.get("HTTP_REFERER", "/"))

# Import submodules for URL routing
from . import hops, styles, fermentables, yeasts, trends, search
