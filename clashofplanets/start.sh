#!/usr/bin/bash


UPDATE_TIME=2

python manage.py runserver &

# Wait 5 seconds until the game loads
sleep 5

while true
do
    sleep $UPDATE_TIME
    python manage.py generate_resources
done
