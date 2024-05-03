#!/bin/bash

rm db.sqlite3
rm -rf ./sniffapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations sniffapi
python3 manage.py migrate sniffapi
python3 manage.py loaddata users
python3 manage.py loaddata categories
python3 manage.py loaddata tags
python3 manage.py loaddata scent_posts
python3 manage.py loaddata scent_tags
python3 manage.py loaddata scent_reviews
python3 manage.py loaddata scent_users
python3 manage.py loaddata favorites
python3 manage.py loaddata tokens
