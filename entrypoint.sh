# #!/bin/sh

# echo "Waiting for postgres..."

# while ! nc -z admin-db 5432; do
#   sleep 0.1
# done

# echo "PostgreSQL started"

# python manage.py recreate_db
# python manage.py seed_db
# # python manage.py runserver -h 0.0.0.0:$PORT
# # gunicorn -b 0.0.0.0:$PORT manage:app
# /home/python/.local/bin/gunicorn --config app/gunicorn_hooks.py --workers 4 --worker-class gevent --preload --timeout 5 --bind 0.0.0.0:$PORT --access-logfile - --log-file - admin:app

#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z shows-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py recreate_db
python manage.py seed_db
gunicorn --config src/admin/gunicorn_hooks.py --workers 4 --worker-class gevent --preload --timeout 5 --bind 0.0.0.0:$PORT --access-logfile - --log-file - manage:app
