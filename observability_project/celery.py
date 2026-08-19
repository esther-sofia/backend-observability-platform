# observability_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set default DJANGO settings module for 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'observability_project.settings')

app = Celery('observability_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.worker_send_task_events = True
app.conf.task_send_sent_event = True
app.conf.task_track_started = True



#from celery.schedules import crontab

#app.conf.beat_schedule = {
    #'heartbeat-every-30-seconds': {
       # 'task': 'observability.tasks.heartbeat',
       # 'schedule': 30.0,
    #},
#}

