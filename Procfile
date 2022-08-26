release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: gunicorn NewsApi_Blogs.wsgi
celery: celery -A NewsApi_Blogs.celery worker --pool=solo -l  info

