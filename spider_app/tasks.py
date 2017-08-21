from celery import shared_task
from django.db import IntegrityError
from django.utils import timezone

from spider_app.models import Item, EntryPoint
from .utils import logger, md5


@shared_task
def add_to_crawler(entry, link, title):
    try:
        Item(url_md5=md5(link), entry=entry,
             url=link, title=title).save()
        logger.info('保存文章 %s', link)
    except IntegrityError:
        pass


@shared_task
def scan_hub():
    logger.info('扫描Hub页Begin')
    for ep in EntryPoint.objects.filter(status=0):
        # logger.info('Hub %s', ep)
        if ep.last_exec_time:
            freq = ep.default_freq if ep.default_freq else 5 * 60
            now = timezone.now()
            if (now - ep.last_exec_time).total_seconds() < freq:
                continue

        from spider_app.worker import parse_hub_entry
        parse_hub_entry(ep)
    logger.info('扫描Hub页Done.')
