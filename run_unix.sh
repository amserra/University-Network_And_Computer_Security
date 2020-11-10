#!/bin/sh
export FLASK_APP=app;
export FLASK_ENV=development;
export SECRET_KEY=`python -c 'import os; print(os.urandom(32))'`;
flask init-db;
flask run