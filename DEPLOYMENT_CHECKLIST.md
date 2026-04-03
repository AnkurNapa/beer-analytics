# Deployment Checklist

## Pre-Deployment (Local Testing)

- [ ] Clone repository
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file from `.env.example`
- [ ] Start PostgreSQL: `brew services start postgresql && createdb beer_analytics`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Load initial data: `python manage.py load_initial_data`
- [ ] Start Django: `python manage.py runserver`
- [ ] Test homepage: http://localhost:8000/ → Shows 6 cards
- [ ] Test styles: http://localhost:8000/styles/ → Shows styles
- [ ] Test search: http://localhost:8000/recipe-search/?q=ipa → Shows results
- [ ] Test unit toggle: Click L/kg/°C button → Switches units
- [ ] All URLs respond (no 404s)

## Railway Deployment Setup

- [ ] Push code to GitHub main branch
- [ ] Create Railway account & new project
- [ ] Add PostgreSQL service to Railway
- [ ] Copy `DATABASE_URL` from Railway to `.env`
- [ ] Generate secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- [ ] Set environment variables in Railway:
  - `DEBUG=False`
  - `SECRET_KEY=<generated-key>`
  - `ALLOWED_HOSTS=*.railway.app`
  - `TIME_ZONE=Asia/Kolkata`
- [ ] Verify Procfile exists (migration + createcachetable commands)
- [ ] Verify runtime.txt exists (python-3.11.9)

## Post-Deployment (Railway Live)

- [ ] Check Railway logs: No errors
- [ ] Test live homepage: https://<your-url>.railway.app/
- [ ] Test styles page: https://<your-url>.railway.app/styles/
- [ ] Test search: https://<your-url>.railway.app/recipe-search/?q=ipa
- [ ] Test unit toggle: Click button, verify session saves
- [ ] Verify PostgreSQL connection: No connection errors in logs
- [ ] Verify static files load: CSS/JS from Tailwind & Plotly CDNs

## Recipe Import (8 Hours)

- [ ] Ensure Django is running on Railway
- [ ] Get `DATABASE_URL` from Railway
- [ ] Export: `export DATABASE_URL="postgres://..."`
- [ ] Run: `bash import_recipes.sh`
- [ ] Monitor progress in separate terminal:
  ```bash
  python manage.py shell
  >>> from recipe_db.models import Recipe
  >>> Recipe.objects.count()  # Should increase over time
  ```

## Post-Import Verification

- [ ] Recipe count: `Recipe.objects.count()` → ~423,000
- [ ] Test search with real recipes: `/recipe-search/?q=ipa` → 10K+ results
- [ ] Test style detail: `/styles/detail/ale/` → Chart loads
- [ ] Test trends: `/trends/` → Charts load with recipe data
- [ ] Verify search performance: Query should complete in <2 seconds
- [ ] Check database size: Rails dashboard shows ~2GB PostgreSQL usage

## Ongoing Monitoring

- [ ] CPU usage: <5% idle
- [ ] Database connections: <10 (free tier max: 20)
- [ ] Error rate in logs: 0% (or fix immediately)
- [ ] Response time: <500ms for overview pages, <3s for charts
- [ ] Weekly: Check Railway billing dashboard (should be $0 with free credits)

## Rollback Plan

If anything breaks:

```bash
# Revert last commit
git revert HEAD
git push origin main

# Railway auto-deploys immediately
# Check logs for recovery
railway logs --tail
```

## Success Criteria

✅ All URLs respond  
✅ Database connected (recipes showing)  
✅ Charts render (Plotly loading)  
✅ Unit toggle works (session saved)  
✅ Search fast (<2s)  
✅ No errors in logs  
✅ Free tier Railway costs $0 extra  

🎉 **Deployment complete!**
