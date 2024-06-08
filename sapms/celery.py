# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sapms.settings')

app = Celery('your_project')

# Using a string here means the worker will not have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task(bind=True)
def train_model(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'retrain-model-every-day': {
        'task': 'aiadmin.tasks.retrain_model',
        'schedule': timedelta(minutes=1),
    },
}

