#!/bin/bash -x

pip3path=`which pip3`

run() {
  $pip3path install -r requirements.txt
  $pip3path install -r requirements_test.txt
  env ENV=test python -m pytest tests
}
run