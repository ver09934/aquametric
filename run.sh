#!/bin/bash

if [ ! -d venv ]; then
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
else
    . venv/bin/activate
fi

export FLASK_ENV=development
export FLASK_APP=aquametric

flask run

