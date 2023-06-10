#!/bin/bash


if [ "${MIGRATE}" = "1" ]; then
	python3 manage.py migrate
fi

if [ "${COLLECTSTATIC}" = "1" ]; then
  python3 manage.py collectstatic --noinput
fi

gunicorn --bind 0.0.0.0:8000 ytbl.wsgi:application --reload
