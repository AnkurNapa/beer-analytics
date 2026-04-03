from django.shortcuts import render
from django.http import JsonResponse
from recipe_db.models import Recipe, Style, Hop
from django.db.models import Count, Avg
from datetime import datetime, timedelta


def trends(request):
    """Display brewing trends"""
    period = request.GET.get("period", "12months")
    context = {"period": period}
    return render(request, "trends.html", context)


def trend_chart(request, chart_type):
    """Return Plotly chart data for trends"""

    if chart_type == "recipes_by_month":
        # Monthly recipe count over last 24 months
        from django.db.models.functions import TruncMonth
        monthly = Recipe.objects.annotate(
            month=TruncMonth("created")
        ).values("month").annotate(
            count=Count("id")
        ).order_by("month")[-24:]

        x_labels = [d["month"].strftime("%Y-%m") if d["month"] else "Unknown" for d in monthly]
        y_values = [d["count"] for d in monthly]

        data = [{
            "x": x_labels,
            "y": y_values,
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Recipes"
        }]
        layout = {
            "title": "Recipes Created Over Time",
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Number of Recipes"},
            "hovermode": "x unified"
        }

    elif chart_type == "top_styles":
        # Top 10 most popular styles
        top_styles = Style.objects.annotate(
            recipe_count=Count("all_recipes")
        ).order_by("-recipe_count")[:10]

        data = [{
            "x": [s.name for s in top_styles],
            "y": [s.recipe_count for s in top_styles],
            "type": "bar",
            "marker": {"color": "rgba(217, 119, 6, 0.8)"}
        }]
        layout = {
            "title": "Top 10 Beer Styles",
            "xaxis": {"title": "Style"},
            "yaxis": {"title": "Number of Recipes"}
        }

    elif chart_type == "abv_trends":
        # Average ABV by year
        from django.db.models.functions import TruncYear
        yearly = Recipe.objects.filter(
            abv__isnull=False
        ).annotate(
            year=TruncYear("created")
        ).values("year").annotate(
            avg_abv=Avg("abv")
        ).order_by("year")[-10:]

        x_labels = [d["year"].strftime("%Y") if d["year"] else "Unknown" for d in yearly]
        y_values = [round(d["avg_abv"], 1) for d in yearly]

        data = [{
            "x": x_labels,
            "y": y_values,
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Average ABV"
        }]
        layout = {
            "title": "Average ABV Trends",
            "xaxis": {"title": "Year"},
            "yaxis": {"title": "Average ABV %"},
            "hovermode": "x unified"
        }

    elif chart_type == "ibu_trends":
        # Average IBU by year
        from django.db.models.functions import TruncYear
        yearly = Recipe.objects.filter(
            ibu__isnull=False
        ).annotate(
            year=TruncYear("created")
        ).values("year").annotate(
            avg_ibu=Avg("ibu")
        ).order_by("year")[-10:]

        x_labels = [d["year"].strftime("%Y") if d["year"] else "Unknown" for d in yearly]
        y_values = [round(d["avg_ibu"], 0) for d in yearly]

        data = [{
            "x": x_labels,
            "y": y_values,
            "type": "scatter",
            "mode": "lines+markers",
            "name": "Average IBU"
        }]
        layout = {
            "title": "Average IBU Trends",
            "xaxis": {"title": "Year"},
            "yaxis": {"title": "Average IBU"},
            "hovermode": "x unified"
        }

    elif chart_type == "popular_hops":
        # Top 10 most used hops
        top_hops = Hop.objects.annotate(
            recipe_count=Count("all_recipes")
        ).order_by("-recipe_count")[:10]

        data = [{
            "x": [h.name for h in top_hops],
            "y": [h.recipe_count for h in top_hops],
            "type": "bar",
            "marker": {"color": "rgba(217, 119, 6, 0.8)"}
        }]
        layout = {
            "title": "Top 10 Hops",
            "xaxis": {"title": "Hop"},
            "yaxis": {"title": "Number of Recipes"}
        }

    elif chart_type == "ebc_distribution":
        # Color (EBC) distribution
        colors = Recipe.objects.filter(
            ebc__isnull=False
        ).values_list("ebc", flat=True)

        if colors:
            data = [{
                "x": list(colors),
                "type": "histogram",
                "nbinsx": 30,
                "marker": {"color": "rgba(217, 119, 6, 0.8)"}
            }]
            layout = {
                "title": "Beer Color Distribution (EBC)",
                "xaxis": {"title": "EBC"},
                "yaxis": {"title": "Number of Recipes"}
            }
        else:
            data = [{"x": [], "y": [], "type": "scatter"}]
            layout = {"title": "No color data available"}

    else:
        return JsonResponse({"error": "Unknown chart type"}, status=400)

    return JsonResponse({"data": data, "layout": layout})
