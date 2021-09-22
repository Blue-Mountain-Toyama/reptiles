#!/bin/bash

python ./src/manage.py makemigrations --settings app.settings.production
python ./src/magage.py migarte --settings app.settings.production
python ./src/magage.py collectstatic --settings app.settings.production
python ./src/manage.py runserver 0.0.0.0:80 --settings app.settings.production

celery -A app worker -l info
