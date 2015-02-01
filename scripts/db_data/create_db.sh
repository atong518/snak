#!/bin/bash

DBDATA_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$DBDATA_DIR/../..

echo "CREATING DB..."
createuser snakd -s
createdb master -O snakd -w

echo "MIGRATING..."
python $ROOT_DIR/manage.py makemigrations
python $ROOT_DIR/manage.py migrate


