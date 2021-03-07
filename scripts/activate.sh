#!/bin/bash -x

PWD=`pwd`
pip3 install virtualenv
pythonpath=`which python3`
venvpath=`which virtualenv`
$venvpath --python=$pythonpath venv
activate () {
    /bin/bash -c ". $PWD/venv/bin/activate; exec /bin/bash -i"
}

activate