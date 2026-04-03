from django.shortcuts import render


def search(request):
    """Search recipes"""
    return render(request, "search.html", {})
