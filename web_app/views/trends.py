from django.shortcuts import render
from django.http import JsonResponse


def trends(request):
    """Trends overview"""
    return render(request, "trends.html", {})


def trend_chart(request, chart_type):
    """Trend chart API"""
    return JsonResponse({"data": [], "layout": {}})
