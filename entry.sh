#!/usr/bin/env bash

rm -f celerybeat.pid

python manage.py collectstatic --no-input
python manage.py migrate


celery -A spider beat -l info -S django &
celery -A spider --concurrency=1 -n worker@%h worker &

nginx

gunicorn -k gevent -b 0.0.0.0:8000 --access-logfile /dev/null spider.wsgi:application

