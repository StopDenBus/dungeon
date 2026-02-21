#!/bin/bash

export DB_HOST='stoppi.gusek.info'
export DB_PORT=32307
export DB='dungeon'
export DB_USER='dungeon'
export DB_PASSWORD='ZpHUAsYRJHTSFIjOhAjkhY3L'
export DB_KEY='8DDHuPehI_gALznNPwlO2SELVDq6Lsank7b4HwMTNJg='

export MYSQL_HOST=${DB_HOST}
export MYSQL_TCP_PORT=${DB_PORT}
export USER=${DB_USER}
export MYSQL_PWD=${DB_PASSWORD}

python/bin/python3 server.py
