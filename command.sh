#!/usr/bin/env bash
set -e

cd /code

wait_count=0
while ! python3 manage.py shell -c "
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('select 1')
    cursor.fetchall()
" 2> /dev/null
do
  echo Wait until DB is ready... $((wait_count += 1))
  sleep 5
done

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput