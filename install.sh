#!/bin/bash

#script to unzip and install db for app
FILENAME=PartNumber-Db-viewer-editor-v3-google_login_oauth2.zip
FILEPATH=PartNumber-Db-viewer-editor-v3-google_login_oauth2
cd ~/Downloads
unzip $FILENAME -d ~/pnve_v3
mkdir ~/pnve_v3/$FILEPATH/tmp
mkdir ~/pnve_v3/$FILENAME/static/js
sqlite3 ~/pnve_v3/$FILEPATH/tmp/pnve3.db < ~/pnve_v3/$FILEPATH/pn_db_default_schema.sql

#delete unzipped in Downloads
rm -rv ~/Downloads/$FILEPATH
