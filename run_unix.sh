#!/bin/sh
pip3 install -r requirements.txt;
source venv/bin/activate;
export FLASK_APP=app:create_app;
export FLASK_ENV=development;
export SECRET_KEY=`python -c 'import os; print(os.urandom(32))'`;
flask init-db;
flask run