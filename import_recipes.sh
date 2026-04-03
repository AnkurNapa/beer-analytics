#!/usr/bin/env bash
set -euo pipefail

echo "==> Cloning recipe archives..."
git clone --depth=1 https://github.com/scheb/brewtoad-beer-recipes.git /tmp/brewtoad 2>/dev/null || true
git clone --depth=1 https://github.com/scheb/brewgr-beer-recipes.git /tmp/brewgr 2>/dev/null || true

echo "==> Loading initial metadata..."
python manage.py load_initial_data

echo "==> Importing Brewtoad recipes (330K — takes ~6h)..."
find /tmp/brewtoad -name "*.xml" 2>/dev/null | while read -r f; do
  id=$(basename "$f" .xml)
  python manage.py load_beerxml_recipe "$f" "brewtoad:$id" 2>/dev/null || true
done

echo "==> Importing BrewGr recipes (93K — takes ~2h)..."
find /tmp/brewgr -name "*.xml" 2>/dev/null | while read -r f; do
  id=$(basename "$f" .xml)
  python manage.py load_beerxml_recipe "$f" "brewgr:$id" 2>/dev/null || true
done

echo "==> Mapping + metrics..."
python manage.py map_styles && python manage.py map_hops
python manage.py map_fermentables && python manage.py map_yeasts
python manage.py calculate_metrics && python manage.py calculate_hop_pairings

echo "==> Building search index..."
python manage.py populate_search_vector

echo "==> Import complete!"
