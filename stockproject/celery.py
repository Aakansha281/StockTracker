from datetime import timezone
import os

from celery import Celery
from django.conf import settings
#from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockproject.settings')

app = Celery('stockproject')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')
app.conf.beat_schedule = {
    #'evry-ten-seconds' : {
         #'task': 'mainapp.tasks.update_stock',
         #'schedule' : 10,
         #'args':(['RELIANCE.NS','BAJAJFINSV.NS'],)
   # },
}
#automatically discover tasks that we have added in tasks.py
app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')