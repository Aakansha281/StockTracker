# StockTracker

1. Start asgi server: python3 manage.py runserver
2. Start celery workers: celery -A stockproject.celery worker --pool=solo -l info
3. Start celery beat: celery -A stockproject beat -l INFO
