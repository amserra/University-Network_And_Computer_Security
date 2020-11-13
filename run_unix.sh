#!/bin/sh

# Set venv
source venv/bin/activate;
pip3 install -r requirements.txt;
# Check if keys file exists
if [ -e $(pwd)/set_keys.sh ]
then
   source ./set_keys.sh
else
   echo "Provide keys"
    exit 0
fi

export FLASK_APP=app:create_app;
export FLASK_ENV=development;
flask init-db;
flask run