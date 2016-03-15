#!/usr/bin/env bash
sudo /etc/init.d/mysql restart
mysql -uroot -e "CREATE DATABASE ask_db;"
mysql -uroot -e "CREATE USER 'ask_user'@'localhost' IDENTIFIED BY 'ask_pwd';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON ask_db.* TO 'ask_user'@'localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"

cd ../ask
python manage.py syncdb
