"""Beer Analytics URL patterns"""
from django.urls import path
from . import views
from .views import search, hops, styles, fermentables, yeasts, trends

urlpatterns = [
    # Main pages
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("units/toggle/", views.toggle_units, name="toggle_units"),

    # Recipe search
    path("recipe-search/", search.search, name="recipe_search"),

    # Hops
    path("hops/", hops.hops_overview, name="hops_overview"),
    path("hops/<str:category_slug>/", hops.hops_category, name="hops_category"),
    path("hops/detail/<str:id>/", hops.hop_detail, name="hop_detail"),
    path("api/hop/<str:id>/chart/<str:chart_type>/", hops.hop_chart, name="hop_chart"),

    # Styles
    path("styles/", styles.styles_overview, name="styles_overview"),
    path("styles/<slug:category_slug>/", styles.style_category, name="style_category"),
    path("styles/detail/<slug:slug>/", styles.style_detail, name="style_detail"),
    path("api/style/<slug:slug>/chart/<str:chart_type>/", styles.style_chart, name="style_chart"),

    # Fermentables
    path("fermentables/", fermentables.fermentables_overview, name="fermentables_overview"),
    path("fermentables/<str:category_slug>/", fermentables.fermentable_category, name="fermentable_category"),
    path("fermentables/detail/<str:id>/", fermentables.fermentable_detail, name="fermentable_detail"),
    path("api/fermentable/<str:id>/chart/<str:chart_type>/", fermentables.fermentable_chart, name="fermentable_chart"),

    # Yeasts
    path("yeasts/", yeasts.yeasts_overview, name="yeasts_overview"),
    path("yeasts/<str:category_slug>/", yeasts.yeast_category, name="yeast_category"),
    path("yeasts/detail/<str:id>/", yeasts.yeast_detail, name="yeast_detail"),
    path("api/yeast/<str:id>/chart/<str:chart_type>/", yeasts.yeast_chart, name="yeast_chart"),

    # Trends
    path("trends/", trends.trends, name="trends"),
    path("api/trend/<str:chart_type>/", trends.trend_chart, name="trend_chart"),
]
