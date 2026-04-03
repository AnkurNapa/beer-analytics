# 🍺 Beer Analytics — Minimal India Edition

A lightweight, India-friendly clone of [beer-analytics.com](https://www.beer-analytics.com) featuring 423K+ beer brewing recipes with metric units (L/kg/°C) as the default.

Built for **deep data analysis without serverless timeouts** — Django's pandas queries run 5–30 seconds, requiring Railway.app instead of Vercel/Netlify.

---

## Features

✅ **423K Recipes** from Brewtoad & BrewGr (public archives)  
✅ **Full-Text Search** via PostgreSQL (replaces Elasticsearch)  
✅ **97 Beer Styles** with BJCP definitions  
✅ **100+ Hops** with alpha acid data  
✅ **60+ Fermentables** (malts, grains, extracts)  
✅ **200+ Yeast Strains** with temperature ranges  
✅ **Analytics Charts** — Plotly.js (no build step needed)  
✅ **Metric-First UI** — Toggle L↔gal, kg↔lb, °C↔°F  
✅ **PostgreSQL + Neon** — Free tier, no timeout  
✅ **Tailwind CSS** — CDN-based, no npm build  

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| **Backend** | Django 5.0 | Mature, batteries-included, fast queries |
| **Database** | PostgreSQL (Neon free) | Free tier, FTS, no timeout (vs MySQL) |
| **Frontend** | Tailwind CSS (CDN) | No build step, responsive, India-friendly |
| **Charts** | Plotly.js (CDN) | Interactive, no backend dependencies |
| **Hosting** | Railway.app | Free tier, no serverless timeout, auto-deploys |
| **Data** | Public BeerXML archives | Brewtoad (330K) + BrewGr (93K) |

---

## Quick Start

### Local Development (15 min)

```bash
# 1. Install
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Set up PostgreSQL (Homebrew)
brew install postgresql
brew services start postgresql
createdb beer_analytics

# 3. Configure
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=dev-key
DATABASE_URL=postgres://postgres@localhost/beer_analytics
EOF

# 4. Migrate & load data
python manage.py migrate
python manage.py load_initial_data

# 5. Run
python manage.py runserver
# Visit: http://localhost:8000/
```

See **[SETUP.md](SETUP.md)** for full deployment guide.

---

## Project Structure

```
beer_analytics/
├── config/                    # Django settings, WSGI, URL routing
│   ├── settings.py           # PostgreSQL, whitenoise, India timezone
│   ├── wsgi.py
│   ├── asgi.py
│   └── urls.py
│
├── recipe_db/                 # Recipe database (copied from scheb/beer-analytics)
│   ├── models.py             # Recipe, Style, Hop, Fermentable, Yeast + SearchVectorField
│   ├── analytics/            # SQL queries (2-line patches: RANDOM(), date_trunc)
│   ├── etl/                  # Data import utilities
│   ├── management/commands/  # load_initial_data, populate_search_vector, etc.
│   └── formulas.py           # ABV, IBU, color conversion functions
│
├── web_app/                   # Views & templates (minimal, India-friendly)
│   ├── views/
│   │   ├── __init__.py       # index, about, toggle_units
│   │   ├── search.py         # PostgreSQL FTS search
│   │   ├── hops.py           # Overview, category filter, detail + charts
│   │   ├── styles.py         # Overview, category, detail + charts
│   │   ├── fermentables.py   # Overview, category, detail + charts
│   │   ├── yeasts.py         # Overview, category, detail + charts
│   │   └── trends.py         # Monthly recipes, ABV/IBU trends, popular hops
│   │
│   ├── templates/             # 11 base + detail templates, Tailwind CSS
│   │   ├── base.html         # Navbar, unit toggle, Plotly/Tailwind CDNs
│   │   ├── index.html        # 6 cards: Styles, Hops, Fermentables, Yeasts, Search, Trends
│   │   ├── search.html       # Recipe search + filters
│   │   ├── hops_overview.html, hop_detail.html
│   │   ├── styles_overview.html, style_detail.html
│   │   ├── fermentables_overview.html, fermentable_detail.html
│   │   ├── yeasts_overview.html, yeast_detail.html
│   │   ├── trends.html
│   │   └── about.html        # Data sources, India-friendly note
│   │
│   ├── context_processors.py # unit_system (metric/imperial) for all templates
│   ├── urls.py               # 46 routes: overview, category, detail, API chart endpoints
│   └── apps.py
│
├── manage.py                  # Django CLI
├── requirements.txt           # Django, psycopg2, pandas, plotly, gunicorn, whitenoise
├── .env.example               # Environment variables template
├── Procfile                   # Railway: gunicorn + release migrations + createcachetable
├── runtime.txt                # Python 3.11.9
├── import_recipes.sh          # Bulk import script (Brewtoad + BrewGr, 8 hours)
├── SETUP.md                   # Local → Railway deployment guide
└── README.md                  # This file
```

---

## Features Breakdown

### 1. **Full-Text Search** (PostgreSQL)

```python
# Search recipes by name/style using websearch
SearchQuery("IPA", search_type="websearch")
# Returns ranked results, no Elasticsearch needed
```

### 2. **Metric Unit System**

Session-based toggle: L/kg/°C ↔ gal/lb/°F

```html
<!-- base.html navbar -->
<form method="post" action="{% url 'toggle_units' %}">
    <button>{% if is_metric %}L/kg/°C{% else %}gal/lb/°F{% endif %}</button>
</form>
```

### 3. **Interactive Charts**

All charts load via JavaScript fetch (no server rendering):

```javascript
fetch('/api/style/ale/chart/trends/')
  .then(r => r.json())
  .then(data => Plotly.newPlot(el, data.data, data.layout))
```

### 4. **Category Filtering**

- **Hops**: Aroma, Bittering, Dual-Purpose
- **Styles**: Ale, Lager, Cider, etc. (97 BJCP)
- **Fermentables**: Grain, Sugar, Extract, Adjunct
- **Yeasts**: Ale, Lager, Wheat, Brett/Bacteria

---

## Data Import (8 Hours)

After deployment, import 423K recipes:

```bash
bash import_recipes.sh
```

**What it does:**
1. Clone Brewtoad (330K) & BrewGr (93K) recipe archives
2. Load BJCP beer style definitions
3. Import each BeerXML recipe (~6 hours Brewtoad, ~2 hours BrewGr)
4. Map recipes to styles, hops, yeasts
5. Calculate ABV, IBU, color metrics
6. Build PostgreSQL full-text search index

---

## Deployment

### Railway.app (Recommended)

**Why not Vercel/Netlify?**
- Django queries take 5–30 seconds (pandas analytics)
- Vercel/Netlify serverless timeout: 10 seconds ❌
- Railway.app: No timeout, free tier ✅

**Steps:**
1. Push to GitHub
2. Railway: Connect repo + add PostgreSQL
3. Set env vars (SECRET_KEY, ALLOWED_HOSTS)
4. Auto-deploys on git push

See [SETUP.md → Phase 2](SETUP.md#phase-2-deploy-to-railway) for details.

---

## Differences from Original

| Aspect | Original | This Clone |
|--------|----------|-----------|
| **DB** | MySQL + Elasticsearch | PostgreSQL + FTS |
| **Frontend** | Bootstrap 5 | Tailwind CSS |
| **Charts** | Syncfusion (paid) | Plotly.js (free) |
| **Hosting** | VPS | Railway.app (serverless-friendly) |
| **Default Units** | US (gal/lb/°F) | Metric (L/kg/°C) |
| **UI Templates** | 47 | 11 (minimal) |
| **Recipe Count** | 1.14M (all sources) | 423K (Brewtoad + BrewGr) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser (User)                        │
│  (Chrome, Safari, Firefox — any OS, no app install needed)  │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/HTTPS
┌────────────────────────────▼────────────────────────────────┐
│                    Railway.app (Hosting)                     │
├────────────────┬────────────────┬──────────────┬─────────────┤
│  gunicorn      │  whitenoise    │  PostgreSQL  │  Redis      │
│  (Django app)  │  (static CSS/  │  (Neon free) │  (cache)    │
│                │   JS, images)  │              │             │
└────────────────┴────────────────┴──────────────┴─────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────┐         ┌──────────┐        ┌─────────────┐
   │ Tailwind │        │ Plotly.js│        │ Django REST │
   │  CSS CDN │        │   CDN    │        │   API JSON  │
   │ (styling)│        │ (charts) │        │ (endpoints) │
   └─────────┘        └──────────┘        └─────────────┘
```

---

## FAQ

### Can I run this locally?

Yes, see [Quick Start](#quick-start). Requires PostgreSQL via Homebrew (`brew install postgresql`).

### How much does Railway.app cost?

**Free tier:** $5/month included credits = perfect for 423K recipes.  
**PostgreSQL:** Neon free tier included (no extra cost).

### Why not use MySQL?

1. Analytics queries use PostgreSQL-specific functions (date_trunc, websearch)
2. MySQL DATE_ADD syntax breaks
3. PostgreSQL FTS is better than Elasticsearch

### How long to import all recipes?

~8 hours on a single Railway dyno. Can run in background while you use the app.

### Can I add more recipes?

Yes — use the BeerXML import command or REST API to add recipes programmatically.

### Is metric the default?

Yes, session defaults to `unit_system=metric`. Users can toggle anytime.

---

## Credits

**Original**: [scheb/beer-analytics](https://github.com/scheb/beer-analytics)  
**Recipe Data**: 
- Brewtoad (330K recipes) — https://github.com/scheb/brewtoad-beer-recipes
- BrewGr (93K recipes) — https://github.com/scheb/brewgr-beer-recipes

**License**: CC BY-SA 4.0 (recipe data), Django MIT (code)

---

## Support

- 📖 Setup help: See [SETUP.md](SETUP.md)
- 🐛 Issues: GitHub Issues
- 💬 Questions: Django Slack, Stack Overflow

---

**Built with ❤️ for brewers, data geeks, and metric-first communities.**
