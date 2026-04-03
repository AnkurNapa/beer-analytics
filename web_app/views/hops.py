from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Hop
from django.db.models import Count


def hops_overview(request):
    """List all hops"""
    hops = Hop.objects.order_by("name")

    context = {
        "hops": hops,
        "hops_count": hops.count(),
    }
    return render(request, "hops_overview.html", context)


def hops_category(request, category_slug):
    """List hops in a specific category (AROMA, BITTERING, DUAL_PURPOSE)"""
    category_map = {
        "aroma": "aroma",
        "bittering": "bittering",
        "dual-purpose": "dual-purpose"
    }

    use_value = category_map.get(category_slug)
    if not use_value:
        hops = Hop.objects.none()
    else:
        hops = Hop.objects.filter(use=use_value).order_by("name")

    context = {
        "hops": hops,
        "hops_count": hops.count(),
    }
    return render(request, "hops_overview.html", context)


def hop_detail(request, id):
    """Display details for a single hop"""
    hop = get_object_or_404(Hop, id=id)

    context = {
        "hop": hop,
        "alpha_acid_min": hop.recipes_alpha_min,
        "alpha_acid_max": hop.recipes_alpha_max,
    }
    return render(request, "hop_detail.html", context)


def hop_chart(request, id, chart_type):
    """Return Plotly chart data for a hop"""
    hop = get_object_or_404(Hop, id=id)

    if chart_type == "alpha_acid":
        # Show average alpha acid levels
        data = [{
            "x": ["Alpha Acid"],
            "y": [hop.recipes_alpha_mean or 0],
            "type": "bar",
            "marker": {"color": "rgba(217, 119, 6, 0.8)"}
        }]
        layout = {
            "title": f"{hop.name} Alpha Acid Profile",
            "xaxis": {"title": ""},
            "yaxis": {"title": "Alpha Acid %"},
        }
    elif chart_type == "style_distribution":
        # Hops used in different styles
        styles = hop.all_recipes.values("associated_styles__name").annotate(count=Count("id")).order_by("-count")[:10]
        data = [{
            "x": [s["associated_styles__name"] or "Unknown" for s in styles],
            "y": [s["count"] for s in styles],
            "type": "bar",
            "marker": {"color": "rgba(217, 119, 6, 0.8)"}
        }]
        layout = {
            "title": f"Top Styles Using {hop.name}",
            "xaxis": {"title": "Style"},
            "yaxis": {"title": "Number of Recipes"},
        }
    else:
        return JsonResponse({"error": "Unknown chart type"}, status=400)

    return JsonResponse({"data": data, "layout": layout})
