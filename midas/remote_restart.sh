#!/bin/bash

# Find the gunicorn process ID
PID=$(ps aux | grep 'gunicorn app:app' | grep -v 'grep' | awk '{print $2}')

# If PID is not empty, kill it
if [ ! -z "$PID" ]; then
    echo "Stopping gunicorn process with PID: $PID"
    kill -TERM $PID
    # Wait a few seconds to ensure the process stops
    sleep 5
else
    echo "No gunicorn process found to stop"
fi

# Start gunicorn again
echo "Starting gunicorn..."
gunicorn app:app

echo "Done."
