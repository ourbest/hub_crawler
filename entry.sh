#!/usr/bin/env bash

celery -A spider beat -l info -S django &
celery -A spider --concurrency=1 -n worker@%h worker &

gunicorn -w 2 -b 0.0.0.0:8000 --access-logfile logs/access.log spider.wsgi:application

