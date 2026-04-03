web: cd ecommerce/afribazaar && gunicorn afribazaar.wsgi --log-file -
release: cd ecommerce/afribazaar && python manage.py migrate && python manage.py collectstatic --noinput
