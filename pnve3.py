# all the imports
import sqlite3
import os
import json
import httplib2
import base64
import jwt
import mimetypes
import oauth2client
import smtplib

from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from contextlib import closing
from oauth2client import client, crypt, tools
from apiclient import errors, discovery

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# configuration
cwd = os.getcwd()
rel_path = os.path.join(cwd, 'tmp/pnve3.db')
DATABASE_PATH = rel_path
DEBUG = True
SECRET_KEY = 'dev_key'
MAIL_USERNAME = 'barnav12@gmail.com'
MAIL_PASS = 'nnpvhcjnuyqyyvlz'
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APP_NAME = 'PNVE_v3'

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)

globvar_table_select = 'tbl1xx'
globvar_cur_user_email = ''

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('pn_db_default_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request_fromdb():
    g.db = connect_db()

@app.teardown_request
def teardown_request_fromdb(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/login')
def login():
    return render_template('login.html')

#Used to select table from database via dropdown form on html side
@app.route('/table_select', methods=['POST'])
def select_table():
    table_data = {}
    global globvar_table_select
    table_data["tbl"] = request.form['tbl_select']
    globvar_table_select = table_data["tbl"]
    flash('Table %s selected' % globvar_table_select)
    return redirect(url_for('show_tblxxx_entries'))

#Main page after login
#View of tbl1xx as default
@app.route('/')
def show_tblxxx_entries():
    if (not session.get('logged_in_admin') and not session.get('logged_in_guest') and not session.get('logged_in_engineer')):
          return redirect(url_for('login'))
    template_data = {}
    select_sql_query = "SELECT * FROM %s" % globvar_table_select
    #cursor_partnumber = g.db.execute('select grp || '-' || substr('00000'||pn,-5,5) || '-' || ver from tbl1xx as partnumber')
    cursor = g.db.execute(select_sql_query)
    query_for_tbl_select = "SELECT name FROM sqlite_master WHERE name LIKE 'tbl%'"
    tbl_select = g.db.execute(query_for_tbl_select)
    template_data["rows"] = cursor.fetchall()
    template_data["tbls"] = map(lambda x: x[0], tbl_select.fetchall())
    template_data["cols"] = list(map(lambda x: x[0], cursor.description))
    template_data["actual_tbl"] = globvar_table_select
    #template_data["pn"] = cursor_partnumber.fetchall()
    return render_template('show_tblxxx_entries.html', **template_data)

#Used to add another row to database. Still need to check several forms for SQL Injection
# Found on / between <hr> tags
@app.route('/addtblxxx', methods=['POST'])
def add_tblxxx_entry():
    sql_add_query = "INSERT INTO %s (grp, ver, value, param, desc, status, rohs, datasheet) \
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)" % globvar_table_select
    g.db.execute(sql_add_query,
        [request.form['grp'], request.form['ver'], request.form['value'], request.form['param'], request.form['desc'],
        request.form['status'], request.form['rohs'], request.form['datasheet']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_tblxxx_entries'))

#Used to delete a row from the database if correct user level logged in.
# Found on / page in a seperate <td> tag in tables
@app.route('/del_tblxxx_entry', methods=['POST'])
def del_tblxxx_entry():
    sql_del_query = "DELETE FROM %s WHERE pn=?" %globvar_table_select
    g.db.execute(sql_del_query,[request.form['delete']])
    g.db.commit()
    flash('Entry was successfully deleted')
    return redirect(url_for('show_tblxxx_entries'))

#Used to delete multiple rows from the database at once.
#Checks for checked checkboxes and sends primary key one at a time to database to delete
#No sql Injection
@app.route('/del_multiple_tblxxx_entry', methods=['POST'])
def del_multiple_tblxxx_entry():
    checkedValues = request.form.getlist('multiple_del[]')
    sql_multiple_del_query = "DELETE FROM %s WHERE pn=?" %globvar_table_select
    for element in checkedValues:
        g.db.execute(sql_multiple_del_query,[element])
        g.db.commit()
    flash('Entries were successfully deleted')
    return redirect(url_for('show_tblxxx_entries'))

#Simular code to main page. Redirects user to new page to modify the current values of selected database rows
@app.route('/mod_tblxxx_entry_page/<pk>')
def mod_tblxxx_entry_page(pk):
    template_data = {}
    select_sql_query = "SELECT * FROM %s" % globvar_table_select
#   cursor_partnumber = g.db.execute('select grp || '-' || substr('00000'||pn,-5,5) || '-' || ver from tbl1xx as partnumber')
    cursor = g.db.execute(select_sql_query)
    query_for_tbl_select = "SELECT name FROM sqlite_master WHERE name LIKE 'tbl%'"
    tbl_select = g.db.execute(query_for_tbl_select)
    template_data["rows"] = cursor.fetchall()
    template_data["tbls"] = map(lambda x: x[0], tbl_select.fetchall())
    template_data["cols"] = list(map(lambda x: x[0], cursor.description))
#   template_data["pn"] = cursor_partnumber_fetchall()
    template_data["pn"] = pk
    return render_template('mod_form.html', **template_data)

#Used to receive values from html form if user level is highest
@app.route('/mod_tblxxx_entry', methods=['POST'])
def mod_tblxxx_entry():
    sql_update_query = "UPDATE %s SET grp = ?, ver = ?, value = ?, param = ?, desc = ?, status = ?, rohs = ?, \
        datasheet = ? WHERE pn = ?" %globvar_table_select
    g.db.execute(sql_update_query, [request.form['grp'], request.form['ver'], request.form['value'], request.form['param'],
        request.form['desc'], request.form['status'], request.form['rohs'], request.form['datasheet'], request.form['modify']])
    g.db.commit()
    flash('New entry was successfully modified')
    return redirect(url_for('show_tblxxx_entries'))

#Check if login is valid google acc and if user has access to app
@app.route('/verify', methods=['POST'])
def verify():
    app_valid_user = "not in db"
    database_data= {}
    id_token_encoded = request.form['id']
    try:
        idinfo = client.verify_id_token(id_token_encoded,"697582317644-j2hlr3cmofm19cjibkm3ka0o5k9uf5ek.apps.googleusercontent.com")
# If multiple clients access the backend server:
        if idinfo['aud'] not in ["697582317644-j2hlr3cmofm19cjibkm3ka0o5k9uf5ek.apps.googleusercontent.com"]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        raise crypt.AppIdentityError("Invalid token")
    userid = idinfo['sub']
    user_email = idinfo['email']
    check_token = idinfo['email_verified']
# check if user has valid google email (check google responce)
    if check_token != True:
        flash('Invalid Email!')
        return redirect(url_for('login'))
    global globvar_cur_user_email
    globvar_cur_user_email = user_email
    quoted_user = "'"+userid+"'"
    quoted_email = "'"+user_email+"'"
# accepting autherized users
    query_get_userid = "SELECT * FROM users"
    cursor = g.db.execute(query_get_userid)
    database_data["users+lvl+email+req"] = cursor.fetchall()
    database_data["users"] = list(map(lambda x: x[0], database_data["users+lvl+email+req"]))
    database_data["lvls"] = list(map(lambda x: x[1], database_data["users+lvl+email+req"]))
    database_data["email"] = list(map(lambda x: x[2], database_data["users+lvl+email+req"]))
    database_data["req"] = list(map(lambda x: x[3], database_data["users+lvl+email+req"]))
    print(database_data["req"])
    for user in database_data["users"]:
        if user == userid:
            query_check_lvl = "SELECT usr_lvl FROM users WHERE google_id = %s" %quoted_user
            get_lvl = g.db.execute(query_check_lvl)
            get_lvl = get_lvl.fetchall()
            get_lvl = list(map(lambda x: x[0], get_lvl))
            if get_lvl != [None]:
# User in database and has permission level set
                app_valid_user = "Has Permission"
                break
            else:
# User is already in database but has no permission
                app_valid_user = "Permission not set"
# If user not in database (no google_id)
    if app_valid_user == "not in db":
        query_add_userinfo = "INSERT INTO users (google_id,usr_email,sent_auth_req_email) VALUES (%s,%s,'No')" \
            %(quoted_user,quoted_email)
        g.db.execute(query_add_userinfo)
        g.db.commit() #userid added to database, but usr_lvl will be added by admin via add_user.html
# Check permission level of user
    query_select_user_level = "SELECT usr_lvl FROM users WHERE google_id = %s" %quoted_user
    selected_users_access_lvl = g.db.execute(query_select_user_level)
    database_data["lvl"] = list(map(lambda x: x[0], selected_users_access_lvl))
# If user has usr_lvl in database
    if app_valid_user == "Has Permission":
        if database_data["lvl"] == [2]:
            session['logged_in_admin'] = True
            flash("You are logged in as a Admin level user!")
            return redirect(url_for('show_tblxxx_entries'))
        elif database_data["lvl"] == [1]:
            flash("You are logged in as a Engineer level user!")
            session['logged_in_engineer'] = True
            return redirect(url_for('show_tblxxx_entries'))
        else:
            session['logged_in_guest'] = True
            flash("You are logged in as a Guest")
            return redirect(url_for('show_tblxxx_entries'))
# If usr_lvl is null in database
    else:
        print( "Request access!")
        session['awaiting_access'] = True
        return redirect(url_for('awaiting_access'))

#Send email
def send_message(to, subject, text):
    """Args:
            to: Email address of receiver
            subject: subject of the email
            text: body of email
    """
    message = MIMEText(text)
    message['to'] = to
    message['from'] = MAIL_USERNAME
    message['subject'] = subject

    print("TEXT:")
    print(message)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(MAIL_USERNAME, MAIL_PASS)
    mailServer.sendmail(MAIL_USERNAME, MAIL_USERNAME, message.as_string())
    mailServer.close()

#If user is not yet in the database. Email is sent to the admin for user level access
@app.route('/awaiting_access')
def awaiting_access():
    #check if email has already been sent
    sent_mail = ''
    query_check_mail_sent = 'SELECT sent_auth_req_email FROM users WHERE usr_email = \'%s\'' %globvar_cur_user_email
    cursor = g.db.execute(query_check_mail_sent)
    g.db.commit()
    sent_mail = cursor.fetchall()
    sent_mail = list(map(lambda x: x[0], sent_mail))
    #Check if email was already sent or not. If yes dont send again
    if sent_mail == ['No']:
        print("No:In Here")
        #message to send
        msg = "New user "+globvar_cur_user_email+" has asked for access"
        #send email for admin to add user to database and set user level via SMTP
        send_message(MAIL_USERNAME,'New user access',msg)
        #change sent_auth_req_email to yes in db
        query_change_email_stat = 'UPDATE users SET sent_auth_req_email=\'Yes\' WHERE usr_email=\'%s\'' %globvar_cur_user_email
        print("CHANGE STAT:",query_change_email_stat)
        g.db.execute(query_change_email_stat)
        g.db.commit()
        return render_template('awaiting_access.html')
    else:
        print("YES: In Here")
        return render_template('awaiting_access.html')

#Backend for displaying user in database and access levels
@app.route('/add_user_page')
def add_user_page():
    if not session.get('logged_in_admin'):
        return redirect(url_for('show_tblxxx_entries'))
    database_data = {}
    query_get_email = "SELECT usr_email FROM users"
    query_select_app_users = 'SELECT usr_email, usr_lvl FROM users WHERE usr_lvl != \'NULL\''
    cursor = g.db.execute(query_get_email)
    database_data['users'] = cursor.fetchall()
    database_data['users'] = list(map(lambda x: x[0], database_data["users"]))
    cursor2 = g.db.execute(query_select_app_users)
    database_data['app_users'] = cursor2.fetchall()
    database_data['cols'] = list(map(lambda x: x[0], cursor2.description))
    print(database_data['app_users'])
    print(database_data['cols'])
    return render_template('add_user.html', **database_data)

@app.route('/add_user',methods=['POST'])
def add_user():
#Check number of admin users before change
    database_data = {}
    query_check_num_admin = "SELECT google_id FROM users WHERE usr_lvl = 2"
    cursor = g.db.execute(query_check_num_admin)
    database_data["num_admin"] = cursor.fetchall()
    admin_count = len(database_data["num_admin"])
    listed_user = "['"+request.form['email']+"']"
    print("Current user: ",globvar_cur_user_email)
    print("request email:",request.form['email'])
# Dont allow change if only 1 admin user and change from admin to other
    if admin_count == 1:
        database_data["admin"] = list(map(lambda x: x[0], database_data["num_admin"]))
        admin = str(database_data["admin"])
        if listed_user == admin:
            flash('User cannot change his own permission level')
            return redirect(url_for('add_user_page'))
# Dont allow user to change his own user level
    if request.form['email'] == globvar_cur_user_email:
        flash('User cannot change his own permission level')
        return redirect(url_for('add_user_page'))
    query_add_user = "UPDATE users SET usr_lvl = ? WHERE usr_email = ?"
    g.db.execute(query_add_user, [request.form['adduser'], request.form['email']])
    g.db.commit()
    flash('User rights level successfully changed')
    return redirect(url_for('add_user_page'))

@app.route('/logout')
def logout():
    session.pop('logged_in_guest', None)
    session.pop('logged_in_engineer', None)
    session.pop('logged_in_admin', None)
    session.pop('awaiting_access', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
