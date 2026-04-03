from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Fermentable
from django.db.models import Count


def fermentables_overview(request):
    """List all fermentables"""
    fermentables = Fermentable.objects.order_by("name")

    context = {
        "fermentables": fermentables,
        "fermentables_count": fermentables.count(),
    }
    return render(request, "fermentables_overview.html", context)


def fermentable_category(request, category_slug):
    """List fermentables in a specific category"""
    category_map = {
        "grain": "grain",
        "sugar": "sugar",
        "fruit": "fruit",
        "extract": "extract",
        "adjunct": "adjunct"
    }

    category_value = category_map.get(category_slug)
    if not category_value:
        fermentables = Fermentable.objects.none()
    else:
        fermentables = Fermentable.objects.filter(category=category_value).order_by("name")

    context = {
        "fermentables": fermentables,
        "fermentables_count": fermentables.count(),
    }
    return render(request, "fermentables_overview.html", context)


def fermentable_detail(request, id):
    """Display details for a single fermentable"""
    fermentable = get_object_or_404(Fermentable, id=id)
    context = {"fermentable": fermentable}
    return render(request, "fermentable_detail.html", context)


def fermentable_chart(request, id, chart_type):
    """Return Plotly chart data for a fermentable"""
    fermentable = get_object_or_404(Fermentable, id=id)

    if chart_type == "usage":
        # Number of recipes using this fermentable
        recipe_count = fermentable.all_recipes.count()
        data = [{
            "labels": ["Used", "Not Used"],
            "values": [recipe_count, max(0, 100 - recipe_count)],
            "type": "pie",
            "marker": {
                "colors": ["rgba(217, 119, 6, 0.8)", "rgba(217, 119, 6, 0.2)"]
            }
        }]
        layout = {
            "title": f"Recipe Usage of {fermentable.name}"
        }

    elif chart_type == "styles":
        # Most common styles using this fermentable
        styles = fermentable.all_recipes.values("associated_styles__name").annotate(
            count=Count("id")
        ).order_by("-count")[:10]

        data = [{
            "x": [s["associated_styles__name"] or "Unknown" for s in styles],
            "y": [s["count"] for s in styles],
            "type": "bar",
            "marker": {"color": "rgba(217, 119, 6, 0.8)"}
        }]
        layout = {
            "title": f"Top Styles Using {fermentable.name}",
            "xaxis": {"title": "Style"},
            "yaxis": {"title": "Number of Recipes"}
        }

    else:
        return JsonResponse({"error": "Unknown chart type"}, status=400)

    return JsonResponse({"data": data, "layout": layout})
