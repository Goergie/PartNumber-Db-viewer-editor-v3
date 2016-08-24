#!/bin/bash

echo Checking all pre-installation requirements

echo Checking pip3
if hash pip3 2>/dev/null; then
    echo Installed!
else
    echo Installing pip3
    sudo apt-get install python3-pip
fi

echo Checking virtualenv
if hash virtualenv 2>/dev/null; then
    echo Installed!
else
    echo Installing virtualenv
    sudo apt-get install python-virtualenv
fi

echo Creating app home
mkdir ~/pnve_v3

cd ~/pnve_v3/venv
source bin/activate
cd ..

echo Checking sqlite3
if hash sqlite3 2>/dev/null; then
    echo Installed!
else
    echo Installing sqlite3
    sudo apt-get install sqlite3
fi

echo Checking python3
if hash python3 2>/dev/null; then
    echo Installed!
else
    echo Installing python3
    sudo apt-get install python3
fi

# function checkpipoutdated {
#     pip list -o | grep -F Flask
#     return output
# }
# checkpip

pip3 install --upgrade pip3
pip3 install --upgrade Flask
pip3 install --upgrade flask-bootstrap
pip3 install --upgrade google-api-python-client
