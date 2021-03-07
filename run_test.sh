#!/bin/sh

pip3 install virtualenv
virtualenv -q -p /usr/bin/python .
source venv/bin/activate
pip3 install -r requirements_test.txt
env ENV=test python -m pytest tests