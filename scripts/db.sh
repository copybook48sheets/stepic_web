#!/usr/bin/env bash
sudo /etc/init.d/mysql restart
mysqld &

mysql -uroot -e "create database if not exists ask_db"
mysql -uroot -e "grant all on ask_db.* to 'ask_user'@'localhost' identified by 'ask_pwd'"

cd ../ask
python manage.py syncdb
