#!/bin/sh

HOST=127.0.0.1:8000
UPDATE_TIME=2
COUNT=0

# When receive a ctrl+c
function ctrl_c() {
    while [ $COUNT -lt 3 ]; do
        echo -e "Waiting until django processes spawn..."
        sleep 2
        COUNT=$(ps ax | grep $HOST | wc -l)
    done

    echo -e Killing django...
    fuser -k 8000/tcp
    exit 0
}

# Catch ctrl+c
trap ctrl_c INT

/usr/bin/python manage.py runserver $HOST &

# Wait 5 seconds until the game loads
sleep 5

# Sleep and run the updates
while true
do
    sleep $UPDATE_TIME
    python manage.py generate_resources
done
