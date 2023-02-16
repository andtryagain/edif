#!/bin/bash

python3 -m venv env
source env/bin/activate
pip install -U -r requirements.txt
export FLASK_APP=./app/app
flask run app -p 3000
