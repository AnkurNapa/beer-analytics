from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Yeast
from django.db.models import Count


def yeasts_overview(request):
    """List all yeasts"""
    yeasts = Yeast.objects.order_by("name")

    context = {
        "yeasts": yeasts,
        "yeasts_count": yeasts.count(),
    }
    return render(request, "yeasts_overview.html", context)


def yeast_category(request, category_slug):
    """List yeasts in a specific category (ALE, LAGER, WHEAT, etc)"""
    category_map = {
        "ale": "ale",
        "lager": "lager",
        "wheat": "wheat",
        "brett-bacteria": "brett-bacteria",
        "wine-cider": "wine-cider"
    }

    type_value = category_map.get(category_slug)
    if not type_value:
        yeasts = Yeast.objects.none()
    else:
        yeasts = Yeast.objects.filter(type=type_value).order_by("name")

    context = {
        "yeasts": yeasts,
        "yeasts_count": yeasts.count(),
    }
    return render(request, "yeasts_overview.html", context)


def yeast_detail(request, id):
    """Display details for a single yeast"""
    yeast = get_object_or_404(Yeast, id=id)
    context = {"yeast": yeast}
    return render(request, "yeast_detail.html", context)


def yeast_chart(request, id, chart_type):
    """Return Plotly chart data for a yeast"""
    yeast = get_object_or_404(Yeast, id=id)

    if chart_type == "usage":
        # Number of recipes using this yeast
        recipe_count = yeast.all_recipes.count()
        data = [{
            "labels": ["Used", "Not Used"],
            "values": [recipe_count, max(0, 100 - recipe_count)],
            "type": "pie",
            "marker": {
                "colors": ["rgba(217, 119, 6, 0.8)", "rgba(217, 119, 6, 0.2)"]
            }
        }]
        layout = {
            "title": f"Recipe Usage of {yeast.name}"
        }

    elif chart_type == "styles":
        # Most common styles using this yeast
        styles = yeast.all_recipes.values("associated_styles__name").annotate(
            count=Count("id")
        ).order_by("-count")[:10]

        data = [{
            "x": [s["associated_styles__name"] or "Unknown" for s in styles],
            "y": [s["count"] for s in styles],
            "type": "bar",
            "marker": {"color": "rgba(217, 119, 6, 0.8)"}
        }]
        layout = {
            "title": f"Top Styles Using {yeast.name}",
            "xaxis": {"title": "Style"},
            "yaxis": {"title": "Number of Recipes"}
        }

    else:
        return JsonResponse({"error": "Unknown chart type"}, status=400)

    return JsonResponse({"data": data, "layout": layout})
