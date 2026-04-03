web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
release: python manage.py migrate --no-input && python manage.py createcachetable cache_table && python manage.py createcachetable cache_table_data
