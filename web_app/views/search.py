from django.contrib.postgres.search import SearchQuery, SearchRank
from django.shortcuts import render
from recipe_db.models import Recipe


class RecipeSearchScope:
    """Encapsulates search criteria"""
    def __init__(self, search_term=None, hop_criteria=None, style_criteria=None):
        self.search_term = search_term
        self.hop_criteria = hop_criteria
        self.style_criteria = style_criteria


def execute_search(scope: RecipeSearchScope):
    """Execute recipe search with PostgreSQL FTS"""
    qs = Recipe.objects.all()

    if scope.search_term:
        # Use PostgreSQL websearch for natural language queries
        query = SearchQuery(scope.search_term, search_type="websearch")
        qs = qs.filter(search_vector=query).annotate(
            rank=SearchRank("search_vector", query)
        ).order_by("-rank")

    if scope.hop_criteria:
        qs = qs.filter(associated_hops__id=scope.hop_criteria)

    if scope.style_criteria:
        qs = qs.filter(associated_styles__id=scope.style_criteria)

    return qs.select_related("style").distinct()[:100]


def search(request):
    """Recipe search view"""
    search_term = request.GET.get("q", "")
    hop_id = request.GET.get("hop", None)
    style_id = request.GET.get("style", None)

    scope = RecipeSearchScope(
        search_term=search_term,
        hop_criteria=hop_id,
        style_criteria=style_id
    )

    results = execute_search(scope) if search_term or hop_id or style_id else []

    context = {
        "search_term": search_term,
        "results": results,
        "result_count": len(results),
    }

    return render(request, "search.html", context)
