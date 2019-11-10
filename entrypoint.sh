# #!/bin/sh

gunicorn --config app/gunicorn_hooks.py --workers 4 --worker-class gevent --preload --timeout 5 --bind 0.0.0.0:$PORT --access-logfile - --log-file - manage:app
