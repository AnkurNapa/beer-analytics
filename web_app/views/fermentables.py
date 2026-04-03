from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Fermentable


def fermentables_overview(request):
    """List all fermentables"""
    fermentables = Fermentable.objects.all().order_by("name")
    return render(request, "fermentables_overview.html", {"fermentables": fermentables})


def fermentable_category(request, category_slug):
    """Fermentables in category"""
    return render(request, "fermentables_overview.html", {})


def fermentable_detail(request, id):
    """Fermentable detail page"""
    return render(request, "fermentable_detail.html", {})


def fermentable_chart(request, id, chart_type):
    """Fermentable chart API"""
    return JsonResponse({"data": [], "layout": {}})
