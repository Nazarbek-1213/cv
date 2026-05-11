#!/usr/bin/env bash
# Render / shu kabi platformalar uchun build script
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --noinput
