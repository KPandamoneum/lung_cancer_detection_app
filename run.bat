@echo off
cd /d %~dp0
python manage.py runserver
start
http://127.0.0.1:8000/home_async