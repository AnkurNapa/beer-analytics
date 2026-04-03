from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Hop


def hops_overview(request):
    """List all hops"""
    hops = Hop.objects.all().order_by("name")
    
    context = {
        "hops": hops,
        "hops_count": hops.count(),
    }
    return render(request, "hops_overview.html", context)


def hops_category(request, category_slug):
    """Hops in category"""
    hops = Hop.objects.filter(category=category_slug).order_by("name")
    
    context = {
        "hops": hops,
        "category": category_slug,
    }
    return render(request, "hops_overview.html", context)


def hop_detail(request, id):
    """Hop detail page"""
    hop = get_object_or_404(Hop, id=id)
    
    context = {
        "hop": hop,
    }
    return render(request, "hop_detail.html", context)


def hop_chart(request, id, chart_type):
    """Hop chart API"""
    return JsonResponse({"data": [], "layout": {}})
