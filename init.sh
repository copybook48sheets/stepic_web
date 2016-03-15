#!/usr/bin/env bash

sudo rm /etc/nginx/sites-enabled/default

sudo ln -s etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
cd /home/box/web
gunicorn -c 0.0.0.0:8080 hello:application &

gunicorn -c 0.0.0.0:80 ask.wsgi --pythonpath '/home/box/web/ask' &
