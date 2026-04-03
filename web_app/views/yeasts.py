from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Yeast


def yeasts_overview(request):
    """List all yeasts"""
    yeasts = Yeast.objects.all().order_by("name")
    return render(request, "yeasts_overview.html", {"yeasts": yeasts})


def yeast_category(request, category_slug):
    """Yeasts in category"""
    return render(request, "yeasts_overview.html", {})


def yeast_detail(request, id):
    """Yeast detail page"""
    return render(request, "yeast_detail.html", {})


def yeast_chart(request, id, chart_type):
    """Yeast chart API"""
    return JsonResponse({"data": [], "layout": {}})
