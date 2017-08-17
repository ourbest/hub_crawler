import logging
import os
import threading
from time import sleep

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spider.settings')

app = Celery('spider')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

logger = logging.getLogger(__name__)


class HubThread(threading.Thread):
    def __init__(self):
        super(HubThread, self).__init__(name="watch")

    def run(self):
        while True:
            try:
                sleep(60)
                from spider_app import tasks
                tasks.scan_hub()
            except:
                logger.warn('hub task error', exc_info=1)


if os.environ.get('C_TASK') == '1':
    HubThread().start()
