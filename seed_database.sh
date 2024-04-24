#!/bin/bash

rm db.sqlite3
rm -rf ./sniffapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations sniffapi
python3 manage.py migrate sniffapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

