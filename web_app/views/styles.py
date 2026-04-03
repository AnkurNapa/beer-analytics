from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Style
from django.db.models import Count, Avg


def styles_overview(request):
    """List all beer styles"""
    styles = Style.objects.all().order_by("name")
    
    context = {
        "styles": styles,
        "styles_count": styles.count(),
    }
    return render(request, "styles_overview.html", context)


def style_category(request, category_slug):
    """Styles in category"""
    styles = Style.objects.filter(parent_style__slug=category_slug).order_by("name")
    
    context = {
        "styles": styles,
        "category": category_slug,
    }
    return render(request, "styles_overview.html", context)


def style_detail(request, slug):
    """Style detail page"""
    style = get_object_or_404(Style, slug=slug)
    
    context = {
        "style": style,
    }
    return render(request, "style_detail.html", context)


def style_chart(request, slug, chart_type):
    """Style chart API"""
    return JsonResponse({"data": [], "layout": {}})
