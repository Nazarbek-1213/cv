#!/usr/bin/env bash
# Render / shu kabi platformalar uchun build script
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --noinput
# Idempotent: seeds the CV (KinoFond, skills, languages, diploma) on every
# build. Existing user-edited content is preserved.
python manage.py seed_cv
