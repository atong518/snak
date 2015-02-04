#!/bin/bash

DBDATA_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$DBDATA_DIR/../..

echo "Loading fake user accounts..."
python $DBDATA_DIR/load_users.py

echo "Loading fake interests..."
python $DBDATA_DIR/load_interests.py