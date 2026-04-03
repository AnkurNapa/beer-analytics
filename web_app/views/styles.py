from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from recipe_db.models import Style, StyleCategory
from django.db.models import Count, Avg


def styles_overview(request):
    """List all beer styles"""
    styles = Style.objects.select_related("category").order_by("name")
    categories = StyleCategory.objects.annotate(
        style_count=Count("style")
    ).order_by("name")

    context = {
        "styles": styles,
        "categories": categories,
        "styles_count": styles.count(),
    }
    return render(request, "styles_overview.html", context)


def style_category(request, category_slug):
    """List styles in a specific category"""
    category = get_object_or_404(StyleCategory, slug=category_slug)
    styles = category.style_set.all().order_by("name")
    categories = StyleCategory.objects.annotate(
        style_count=Count("style")
    ).order_by("name")

    context = {
        "styles": styles,
        "categories": categories,
        "category": category,
        "styles_count": styles.count(),
    }
    return render(request, "styles_overview.html", context)


def style_detail(request, slug):
    """Display details for a single beer style"""
    style = get_object_or_404(Style, slug=slug)
    context = {"style": style}
    return render(request, "style_detail.html", context)


def style_chart(request, slug, chart_type):
    """Return Plotly chart data for a style"""
    style = get_object_or_404(Style, slug=slug)

    if chart_type == "trends":
        # Recipes of this style over time (months)
        monthly_data = style.all_recipes.values("created__year", "created__month").annotate(
            count=Count("id")
        ).order_by("created__year", "created__month")[:24]

        x_labels = [f"{d['created__year']}-{d['created__month']:02d}" for d in monthly_data]
        y_values = [d["count"] for d in monthly_data]

        data = [{
            "x": x_labels,
            "y": y_values,
            "type": "bar",
            "marker": {"color": "rgba(217, 119, 6, 0.8)"}
        }]
        layout = {
            "title": f"{style.name} Recipes Over Time",
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Number of Recipes"},
            "hovermode": "x"
        }

    elif chart_type == "abv":
        # ABV distribution for this style
        recipes = style.all_recipes.exclude(abv__isnull=True).values_list("abv", flat=True)
        if recipes:
            data = [{
                "x": list(recipes),
                "type": "histogram",
                "nbinsx": 20,
                "marker": {"color": "rgba(217, 119, 6, 0.8)"}
            }]
            avg_abv = sum(recipes) / len(recipes)
            layout = {
                "title": f"{style.name} ABV Distribution (avg: {avg_abv:.1f}%)",
                "xaxis": {"title": "ABV %"},
                "yaxis": {"title": "Number of Recipes"},
            }
        else:
            data = [{"x": [], "y": [], "type": "scatter"}]
            layout = {"title": f"No ABV data for {style.name}"}

    else:
        return JsonResponse({"error": "Unknown chart type"}, status=400)

    return JsonResponse({"data": data, "layout": layout})
