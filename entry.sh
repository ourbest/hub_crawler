#!/usr/bin/env bash

rm -f celerybeat.pid

celery -A spider beat -l info -S django &
celery -A spider --concurrency=1 -n worker@%h worker &

gunicorn -k gevent -b 0.0.0.0:8000 --access-logfile logs/access.log spider.wsgi:application

