# setup Database
python3 manage.py makemigrations be_auth_model
python3 manage.py makemigrations oauth
python3 manage.py makemigrations mfa
python3 manage.py migrate

# setup admin page (static file, superuser)
python3 manage.py collectstatic --noinput
export $(cat ${DJANGO_SUPERUSER})
python3 manage.py createsuperuser --noinput

gunicorn -b 0.0.0.0:8000 be_auth.wsgi:application