import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from spider_app import utils
from spider_app.models import Item, EntryPoint
from spider_app.utils import logger

_sess = None


def _get_session(domain):
    global _sess
    if not _sess:
        _sess = requests.session()
    return _sess


def crawler(url):
    if _check_dup(url):
        return

    parsed_uri = urlparse(url)
    sess = _get_session(parsed_uri.netloc)
    return sess.get(url)


def _get_title(entry, bs):
    if entry.title_selector:
        pass

    return bs.find('title').get_text()


def _get_content(entry, bs):
    return str(bs.find('body'))


def get_content(entry, url):
    resp = crawler(url)
    if resp:
        bs = BeautifulSoup(resp.content, "lxml")
        Item(entry=entry, url_md5=utils.md5(url), url=url,
             title=_get_title(entry, bs), content=_get_content(entry, bs)).save()


def parse_hub(hub_id):
    entry = EntryPoint.objects.filter(id=hub_id).first()
    if entry:
        parse_hub_entry(entry)


def parse_hub_entry(entry):
    logger.info("抓取HUB页 %s", entry.name)
    entry.last_exec_time = timezone.now()
    entry.save()
    resp = crawler(entry.url)
    if resp:
        old_items = [x.url for x in entry.item_set.order_by("-pk")[0:100]]
        # if not resp.encoding:
        #     resp.encoding = 'utf-8'
        bs_article = BeautifulSoup(resp.content, "lxml")
        for link in bs_article.find_all("a"):
            if link.has_attr('href'):
                title = link.get_text()
                link = link['href']
                if title and link not in old_items and re.search(entry.url_pattern, link):
                    from .tasks import add_to_crawler
                    add_to_crawler.delay(entry, link, title)


def _check_dup(url):
    return Item.objects.filter(url_md5=utils.md5(url)).first() is not None
