#!/usr/bin/env bash
sudo python3 manage.py runserver 0.0.0.0:80

kill -INT 888

sleep 30

./runserver.sh