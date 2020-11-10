#!/bin/sh
set FLASK_APP=app;
set FLASK_ENV=development;
set SECRET_KEY=`python -c 'import os; print(os.urandom(32))'`;
flask init-db;
flask run