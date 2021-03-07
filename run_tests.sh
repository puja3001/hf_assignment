#!/bin/bash -x

PWD=`pwd`
pythonpath=`which python3`
venvpath=`which virtualenv`
pip3path=`which pip3`
$venvpath --python=$pythonpath venv
echo $PWD
activate () {
    . $PWD/venv/bin/activate
}

run() {
  $pip3path install -r requirements.txt
  $pip3path install -r requirements_test.txt
  env ENV=test python -m pytest tests
}

activate
run