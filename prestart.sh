#!/usr/bin/env sh

python manage.py migrate
python manage.py collectstatic --noinput

# Uncomment the following if you use i18n
#python manage.py compilemessages
