# PartNumber-Db-viewer-editor-v3

## Description and Motivation  
A database management app designed by me to learn python flask
## Installation
### Pre-requirements
*All requirements will be checked and downloaded with the requirements.sh script. Run script to check if your system has all needed programs and python modules. It will download all that are not downloaded, so sudo or superuser permission is needed. Install.sh script unzips the downloaded .zip file and moves it to the needed location and creates the needed folders. The list below only list the requirements for user information*
- python3-pip  
- Google api client.  
- Python3  
- Sqlite3  
- [jquery Idle](https://github.com/kidh0/jquery.idle.git)  
- Flask  
- Bootstrap-flask  

#### After Pre-requirements are met do the following steps:
(*Steps for Ubuntu*)  
1. Clone or download the repo  
2. Unzip in Downloads (install script will delete later)  
3. Run the requirements.sh script  
`cd ~/Downloads/PartNumber-Db-viewer-editor-v3-google_login_oauth2/` then `./requirements.sh`  
4. Run the install.sh script  
`./install.sh`  
5. Download [jquery.idle](https://github.com/kidh0/jquery.idle.git)  
6. Move the unzipped folder (jquery.ilde-master) to the js folder created by the install.sh script  
location: ~/pnve_v3/PartNumber-Db-viewer-editor-v3-google_login_oauth2/static/js  
5. Open a terminal cd into the folder of app  
`cd ~/pnve_v3/PartNumber-Db-viewer-editor-v3-google_login_oauth2/`  
6. Run the python script.  
`python3 pnve3.py` (*Please note that the config and client secret files are also needed for the app to run*)

## Tests
Requirements and install script tested on a VM using a clean Xubuntu 16.04 Image, with partical requirements met and all requirements met.  
Manual tests done for the python app  
Unit Tests are under construction  
Front end tests done on Mozilla Firefox 47.0 and Google Chrome Version 52.0.2743.116 (64-bit)

##TO-DO:
- Remove all global variables  
- Improve session security  
- Add order by on columns  
- Keep table view on current table after modifications/deletions (Reverts back to tbl1xx view atm)  
- Search option  
- Make partnumber equal grp+pn+ver  

## Licences
**See Licences for pre-installation requirements**  
