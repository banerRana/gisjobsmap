#!/bin/bash

GEOLITE2=GeoLite2-City

if [ ! -f /app/data/${GEOLITE2}.mmdb ]; then
    echo "extracting ${GEOLITE2}.zip"
    unzip -o /app/data/${GEOLITE2}.zip -d /app/data
fi

if [  "${FLASK_ENV}" = "development" ]; then
  python manage.py run --host 0.0.0.0 --port 5000
else
  gunicorn 'api:create_app()' -b 0.0.0.0:5000 --workers=4
fi