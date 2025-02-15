python3 manage.py makemigrations be_auth_model
python3 manage.py makemigrations oauth
python3 manage.py makemigrations mfa
python3 manage.py migrate

gunicorn -b 0.0.0.0:8000 be_auth.wsgi:application