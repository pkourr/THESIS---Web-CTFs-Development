#!/bin/sh

# Generate global variables
export APP_SECRET_KEY=$(python3.8 -c 'import secrets;print(secrets.token_hex(32))' 2>&1)

# Start HAProxy in the background
haproxy -f /usr/local/etc/haproxy/haproxy.cfg &

# Serve application with Gunicorn using Gevent workers
python3.8 -m gunicorn --keep-alive 10 -k gevent --bind 0.0.0.0:$APP_PORT -w 20 app:app


