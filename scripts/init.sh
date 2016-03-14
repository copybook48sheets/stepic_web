#!/usr/bin/env bash

sudo rm /etc/nginx/sites-enabled/default

sudo ln -s etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

gunicorn -c /home/box/web/etc/gunicorn_conf.py hello:application &

gunicorn -c /home/box/web/etc/gunicorn_django_conf.py ask.wsgi --pythonpath '/home/box/web/ask' &
