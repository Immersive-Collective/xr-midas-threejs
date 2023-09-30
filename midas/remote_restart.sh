#!/bin/bash

#bash: ssh username@remote_server_ip 'bash -s' < /path_to/manage_gunicorn.sh

SCREEN_NAME="gunicorn_screen"

# Check if the screen session exists
screen -list | grep "$SCREEN_NAME"
if [ $? -eq 0 ]; then
    echo "Screen session found. Sending commands to terminate and restart gunicorn."

    # Send Ctrl+C to terminate gunicorn
    screen -S "$SCREEN_NAME" -X stuff '^C'
    sleep 2

    # Send command to restart gunicorn
    screen -S "$SCREEN_NAME" -X stuff 'gunicorn app:app\n'
else
    echo "No screen session named $SCREEN_NAME found. Starting a new one."
    screen -S "$SCREEN_NAME" -dm bash -c 'gunicorn app:app'
fi

echo "Done."
