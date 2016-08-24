#!/bin/bash
FILEPATH=PartNumber-Db-viewer-editor-v3-google_login_oauth2
echo Checking all pre-installation requirements

echo Checking pip3
if hash pip3 2>/dev/null; then
    echo Installed!
else
    echo Installing pip3
    sudo apt-get install python3-pip
fi

echo Creating app home
mkdir ~/pnve_v3
#jquery.idle folder
mkdir ~/pnve_v3/$FILEPATH/static/js

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

pip3 install --upgrade pip3
pip3 install --upgrade Flask
pip3 install --upgrade flask-bootstrap
pip3 install --upgrade google-api-python-client
