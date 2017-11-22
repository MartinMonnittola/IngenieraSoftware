#!/usr/bin/env bash


# When receive a ctrl+c
function ctrl_c() {
        kill -SIGTERM -$$
}

usage () {
    echo "Usage: $0 [-l IP:PORT] [-u SECONDS]"
}

main() {

    # Default options
    HOST=127.0.0.1:8000
    UPDATE_TIME=2

    while getopts "l:u:h" opt; do
        case ${opt} in
            l )  HOST=$OPTARG
                 ;;
            u )  UPDATE_TIME=$OPTARG
                 ;;
            h )  usage
                 exit 0
                 ;;
            \? ) usage
                 exit 1
                 ;;
        esac
    done

    if [[ "$HOST" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+$ ]] &&
       [[ "$UPDATE_TIME" =~ [0-9]+ ]]; then
        # Catch ctrl+c
        trap ctrl_c INT

        # Execute the game
        python manage.py runserver $HOST &

        # Wait for UPDATE_TIME seconds and run the updates
        while true
        do
            sleep $UPDATE_TIME
            python manage.py missiles
            python manage.py generate_resources
        done
    else
        echo "Wrong parameters format. Exiting..."
    fi
}

main $@
