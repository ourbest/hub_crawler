import os
import threading
from time import sleep

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spider.settings')

app = Celery('spider')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


class HubThread(threading.Thread):
    def __init__(self):
        super(HubThread, self).__init__(name="watch")

    def run(self):
        while True:
            sleep(60)
            from spider_app import tasks
            tasks.scan_hub.delay()

if os.environ.get('C_TASK') == '1':
    HubThread().start()