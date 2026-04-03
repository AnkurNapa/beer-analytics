from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from recipe_db.models import Recipe


class Command(BaseCommand):
    help = "Populate search_vector field for all recipes using PostgreSQL full-text search"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Building search index..."))

        # Update all recipes with search vector
        # Weights: name gets highest weight (A), style_raw gets lower weight (B)
        Recipe.objects.all().update(
            search_vector=(
                SearchVector("name", weight="A") +
                SearchVector("style_raw", weight="B") +
                SearchVector("author", weight="C")
            )
        )

        recipe_count = Recipe.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"✓ Search index built for {recipe_count} recipes")
        )
