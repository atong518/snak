#!/bin/bash

DBDATA_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$DBDATA_DIR/../..

echo "Loading users..."
python $DBDATA_DIR/load_users.py