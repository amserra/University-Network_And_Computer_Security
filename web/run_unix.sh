#!/bin/sh

# Set venv
source venv/bin/activate;
pip3 install -r requirements.txt | grep -v 'already satisfied';

export FLASK_ENV=development
flask run