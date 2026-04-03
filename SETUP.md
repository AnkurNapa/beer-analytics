# Beer Analytics Minimal Clone — Setup Guide

**Stack**: Django 5 + PostgreSQL + Tailwind CSS + Plotly.js  
**Hosting**: Railway.app (free tier, no serverless timeout)  
**Data**: 423K recipes (Brewtoad 330K + BrewGr 93K)

---

## Phase 1: Local Development Setup

### 1.1 Clone & Install

```bash
cd /Users/ankur/beer_analytics
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1.2 Create Local PostgreSQL (Homebrew)

```bash
brew install postgresql
brew services start postgresql
createdb beer_analytics
```

Verify PostgreSQL is running:
```bash
pg_isready
# Output: accepting connections
```

### 1.3 Configure .env

```bash
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=local-dev-key-change-in-production
DATABASE_URL=postgres://postgres@localhost/beer_analytics
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=Asia/Kolkata
EOF
```

### 1.4 Run Migrations

```bash
python manage.py migrate
python manage.py createcachetable
```

### 1.5 Load Initial Data

```bash
python manage.py load_initial_data
```

This creates 97 beer styles, 100+ hops, 60+ fermentables, 200+ yeasts from CSV files.

### 1.6 Start Django

```bash
python manage.py runserver
```

**Test URLs:**
- Home: http://localhost:8000/
- Styles: http://localhost:8000/styles/
- Hops: http://localhost:8000/hops/
- Search: http://localhost:8000/recipe-search/?q=ipa
- Trends: http://localhost:8000/trends/

---

## Phase 2: Deploy to Railway

### 2.1 Create Railway Account & Project

1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project → "Deploy from GitHub repo"
4. Connect your beer-analytics repo

### 2.2 Add PostgreSQL Database

1. In Railway dashboard: **+ Add Service**
2. Select **PostgreSQL**
3. Railway auto-injects `DATABASE_URL` environment variable

### 2.3 Set Environment Variables

In Railway project settings, add:

```
DEBUG=False
SECRET_KEY=<generate-strong-key: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
ALLOWED_HOSTS=*.railway.app
TIME_ZONE=Asia/Kolkata
```

### 2.4 Deploy

```bash
git add .
git commit -m "Deploy to Railway: views, URLs, templates complete"
git push origin main
```

Railway auto-deploys from main branch. Watch logs:

```bash
railway up --detach  # Or use Railway dashboard
```

### 2.5 Verify Deployment

```bash
# Check logs
railway logs

# Test live URL
curl https://<your-railway-url>.railway.app/
```

---

## Phase 3: Import Recipes (8 Hours)

### 3.1 Point to Railway Database

```bash
# Get DATABASE_URL from Railway dashboard
export DATABASE_URL="postgres://user:pass@host:5432/db"

# Verify connection
python manage.py dbshell
```

### 3.2 Run Bulk Import

```bash
# Make script executable
chmod +x import_recipes.sh

# Run import (takes ~8 hours)
bash import_recipes.sh
```

**Progress:**
- Brewtoad (330K recipes): ~6 hours
- BrewGr (93K recipes): ~2 hours
- Mapping + metrics: ~30 min
- Search indexing: ~10 min

**What happens:**
```
✓ Clone recipe archives from GitHub
✓ Load BJCP styles, hop data, yeast database
✓ Import each BeerXML recipe
✓ Map recipes to styles, hops, yeasts
✓ Calculate ABV, IBU, color metrics
✓ Build PostgreSQL full-text search index
```

### 3.3 Monitor Import (Optional)

In a separate terminal:

```bash
# Check recipe count
python manage.py shell
>>> from recipe_db.models import Recipe
>>> Recipe.objects.count()
```

---

## Phase 4: Verify All Features

### 4.1 Database Fully Loaded

- [ ] `/styles/` — Shows 97+ styles with filter by category
- [ ] `/hops/` — Shows 100+ hops, filter by use (aroma/bittering)
- [ ] `/fermentables/` — Shows 60+ grains, sugars, extracts
- [ ] `/yeasts/` — Shows 200+ yeast strains
- [ ] `/recipe-search/?q=ipa` — Returns 10K+ IPA recipes via FTS
- [ ] `/trends/` — Charts load with 423K recipe data

### 4.2 Charts Render

Click any detail page (e.g., `/styles/detail/ale/`) and verify Plotly charts load:

```javascript
// Browser console should show:
// ✓ Chart data loaded from /api/style/ale/chart/trends/
// ✓ Plotly.newPlot() called successfully
```

### 4.3 Unit Toggle Works

Click **L/kg/°C** button in navbar:

- [ ] Metric → Imperial: liters → gallons, kg → lbs, °C → °F
- [ ] Imperial → Metric: reverses
- [ ] Persists in session

---

## Phase 5: Troubleshooting

### PostgreSQL Connection Error

```
psycopg2.OperationalError: could not connect to server
```

**Fix:**
```bash
# Check PostgreSQL is running
brew services list  # Should show postgresql started

# Start if stopped
brew services start postgresql

# Create missing database
createdb beer_analytics
```

### Search Index Missing

```
django.db.utils.ProgrammingError: column "search_vector" does not exist
```

**Fix:**
```bash
python manage.py migrate  # Apply SearchVectorField migration
python manage.py populate_search_vector  # Index existing recipes
```

### Slow Recipe Import

```bash
# Run import with batch size optimization
python manage.py load_beerxml_recipe file.xml brewtoad:id --batch-size=100
```

### Charts Not Loading

```bash
# Check API endpoints
curl http://localhost:8000/api/style/ale/chart/trends/

# Should return JSON:
# {"data": [...], "layout": {...}}
```

If 404, verify URL routing in `web_app/urls.py`.

---

## Phase 6: Post-Launch Checklist

### Scale & Performance

- [ ] Set `DEBUG=False` in production
- [ ] Enable HTTPS only (Railway auto-enables)
- [ ] Configure allowed hosts (done via ALLOWED_HOSTS)
- [ ] Run `python manage.py collectstatic` (whitenoise handles this)

### Monitoring

Railway provides free monitoring:
- [ ] Monitor CPU usage (should be <5% idle)
- [ ] Check database connections (max 20 on free tier)
- [ ] Review error logs weekly

### Optional Enhancements

- [ ] Add recipe detail page (view full recipe ingredients)
- [ ] Implement recipe clone/fork (logged-in users)
- [ ] Add brewing calculator for metric/imperial conversions
- [ ] Email alerts on new trends

---

## Quick Reference

| Command | What it does |
|---------|------------|
| `python manage.py runserver` | Start Django locally |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py load_initial_data` | Load BJCP styles, hops, yeasts |
| `bash import_recipes.sh` | Import 423K recipes (8 hours) |
| `python manage.py populate_search_vector` | Index recipes for full-text search |
| `railway up` | Deploy to Railway |
| `railway logs` | Watch deployment logs |

---

## Data Sources

- **Brewtoad**: https://github.com/scheb/brewtoad-beer-recipes (330K recipes, BeerXML, archived)
- **BrewGr**: https://github.com/scheb/brewgr-beer-recipes (93K recipes, BeerXML, archived)
- **BJCP Standards**: Official beer style definitions (97 styles)
- **Hop Data**: Hopsteiner, Yakima Chief, BarthHaas, Crosby archives

All data is publicly available & CC BY-SA 4.0 licensed.

---

## Architecture

```
GitHub (code) ──> Railway.app
                    ├─ gunicorn (Django app)
                    ├─ PostgreSQL (Neon free tier)
                    └─ whitenoise (static files)

Browser (HTTP) ──> Railway URL
                    ├─ Tailwind CSS (CDN)
                    ├─ Plotly.js (CDN)
                    └─ Django views (JSON + HTML)
```

**No serverless timeout** — Railway runs long queries (5-30s) without timeout like Vercel/Netlify.

---

**Estimated time to full launch:**

| Phase | Time |
|-------|------|
| Setup & local test | 15 min |
| Railway deploy | 5 min |
| Initial data load | 30 min |
| Recipe import | **8 hours** |
| **TOTAL** | **~8.5 hours** |

You can test all features after phase 4 (initial data) while recipes import in background.
