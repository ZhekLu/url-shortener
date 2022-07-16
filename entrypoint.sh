#!/bin/sh

echo "Collect static..."
python manage.py collectstatic --noinput
echo "Done."


#python manage.py flush --no-input
python manage.py makemigrations --no-input
python manage.py migrate

python manage.py runserver 0.0.0.0:$PORT

exec "$@"

