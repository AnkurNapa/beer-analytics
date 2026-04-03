# Generated migration for SearchVectorField

from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_db', '0015_searchindexupdatequeue'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='search_vector',
            field=SearchVectorField(null=True, editable=False),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=GinIndex(fields=['search_vector'], name='recipe_search_gin_idx'),
        ),
    ]
