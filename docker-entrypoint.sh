#!/bin/sh
set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

if [ -z "$MODEM_URL" ]; then
    echo "MODEM_URL environment variable is required" >&2
    exit 1
fi

CMD="python examples/sms_http_api.py $MODEM_URL --host $HOST --port $PORT"
if [ -n "$USERNAME" ]; then
    CMD="$CMD --username $USERNAME"
fi
if [ -n "$PASSWORD" ]; then
    CMD="$CMD --password $PASSWORD"
fi
exec $CMD
