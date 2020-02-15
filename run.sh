#!/bin/bash

. venv/bin/activate

export FLASK_ENV=development
export FLASK_APP=aquametric

flask run
