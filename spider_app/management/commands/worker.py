import logging
from time import sleep

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Worker started")
        while True:
            try:
                from spider_app import tasks
                tasks.scan_hub()
            except:
                logger.warning('hub task error', exc_info=1)

            sleep(60)
