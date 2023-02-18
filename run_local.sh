#!/bin/bash

cd app
mkdir upload result
python3 -m venv env
source env/bin/activate
pip install -U -r requirements.txt
export FLASK_APP=app
flask run -p 3000
