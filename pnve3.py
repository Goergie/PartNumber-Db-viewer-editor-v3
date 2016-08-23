# all the imports
import sqlite3
import os
import json
import httplib2
import base64
#import jwt
import mimetypes
import oauth2client
import smtplib
import config

from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from contextlib import closing
from oauth2client import client, crypt, tools
from apiclient import errors, discovery


app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

#global variables
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

#Renders login page. Google acc login login. Login button rendered on front end
@app.route('/login')
def login():
    return render_template('login.html')

#Used to select table from database via dropdown form
@app.route('/table_select', methods=['POST'])
def select_table():
    table_data = {}
    global globvar_table_select
    table_data["tbl"] = request.form['tbl_select']
    globvar_table_select = table_data["tbl"]
    flash('Table %s selected' % globvar_table_select)
    return redirect(url_for('show_tblxxx_entries'))

#Displaying Admin Table management page
@app.route('/table_management')
def mod_table_page():
    if not session.get('logged_in_admin'):
#TO-DO: add html error page access denied!
        return redirect(url_for('show_tblxxx_entries'))
    database_data = {}
    query_for_tbl_select = "SELECT name FROM sqlite_master WHERE name LIKE 'tbl%'"
    cursor = g.db.execute(query_for_tbl_select)
    database_data["tbls"] = map(lambda x: x[0], cursor.fetchall())
    return render_template('mod_table.html', **database_data)

#Adding column to table in db
@app.route('/add_column', methods=['POST'])
def add_column():
    if not session.get('logged_in_admin'):
#TO-DO: add html error page access denied!
        return redirect(url_for('show_tblxxx_entries'))
    table = request.form['tblselect']
    if table == '':
        flash('Please select table')
        return(redirect(url_for('mod_table_page')))
    name = request.form['col_name']
    if name == '':
        flash('Please enter column name')
        return(redirect(url_for('mod_table_page')))
    col_type = request.form['type']
    if col_type == '':
        flash('Please select column type')
        return(redirect(url_for('mod_table_page')))
    # if request.form['notnull'] == "Yes":
    #     null='not null'
    # else:
    #     null = 'null'
    # print("Is null:,null)
    query_mod_table = "ALTER TABLE %s ADD COLUMN %s %s" %(table,name,col_type)
    g.db.execute(query_mod_table)
    g.db.commit()
    flash('Table updated')
    return redirect(url_for('mod_table_page'))

#Column name lister
def select_tbl_header(table):
    '''Arg: table: table for listing all table header names
       Returns: List of the headers
    '''
    select_sql_query = "SELECT * FROM %s LIMIT 1" %table
    cursor = g.db.execute(select_sql_query)
    table_col_names = list(map(lambda x: x[0], cursor.description))
    table_col_names.remove('pn')
    return table_col_names

#Main page after login
@app.route('/')
def show_tblxxx_entries():
    if (not session.get('logged_in_admin') and not session.get('logged_in_guest') and not session.get('logged_in_engineer')):
          return redirect(url_for('login'))
    template_data = {}
    select_sql_query = "SELECT * FROM %s" % globvar_table_select
    cursor = g.db.execute(select_sql_query)
    query_for_tbl_select = "SELECT name FROM sqlite_master WHERE name LIKE '%tbl%'"
    tbl_select = g.db.execute(query_for_tbl_select)
    template_data["rows"] = cursor.fetchall()
    template_data["tbls"] = map(lambda x: x[0], tbl_select.fetchall())
    template_data["cols"] = list(map(lambda x: x[0], cursor.description))
    template_data["actual_tbl"] = globvar_table_select
    return render_template('show_tblxxx_entries.html', **template_data)

#Used to add another row to database.
@app.route('/addrow', methods=['POST'])
def add_tblxxx_entry():
    col = select_tbl_header(globvar_table_select)
    form_request = []
    query=''
    query_end=''
    for x in range(len(col)):
        form_request.append(request.form[col[x]])
    for x in range(len(col)):
        query = query+col[x]+", "
    query_start = "INSERT INTO %s " %globvar_table_select
    query_middle = "("+query[:(len(query)-2)]+")"+" VALUES "
    for x in range(len(col)):
        query_end = query_end+"?, "
    query_end = "("+query_end[:(len(query_end)-2)]+")"
    sql_update_query = query_start+query_middle+query_end
    g.db.execute(sql_update_query, form_request)
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_tblxxx_entries'))

#Checks for checked checkboxes and sends primary key, one at a time to database to delete
@app.route('/del_multiple_tblxxx_entry', methods=['POST'])
def del_multiple_tblxxx_entry():
    checkedValues = request.form.getlist('multiple_del[]')
    sql_multiple_del_query = "DELETE FROM %s WHERE pn=?" %globvar_table_select
    for element in checkedValues:
        g.db.execute(sql_multiple_del_query,[element])
        g.db.commit()
    if len(checkedValues) == 1:
        flash('Entry was successfully deleted')
    else:
        flash('Entries were successfully deleted')
    return redirect(url_for('show_tblxxx_entries'))

#Redirects user to new page to modify the current values of selected database rows
@app.route('/mod_tblxxx_entry_page/<pk>')
def mod_tblxxx_entry_page(pk):
    if not session.get('logged_in_admin'):
#TO-DO: add html error page access denied!
        return redirect(url_for('show_tblxxx_entries'))
    template_data = {}
    select_sql_query = "SELECT * FROM %s" % globvar_table_select
    select_row_elements = "SELECT * FROM %s WHERE pn = %s" %(globvar_table_select,pk)
    print(select_row_elements)
    query_for_tbl_select = "SELECT name FROM sqlite_master WHERE name LIKE 'tbl%'"
    element_select = g.db.execute(select_row_elements)
    cursor = g.db.execute(select_sql_query)
    tbl_select = g.db.execute(query_for_tbl_select)
# All records in selected table are saved in this variable
    template_data["rows"] = cursor.fetchall()
# Tables name are saved in this variable
    template_data["tbls"] = map(lambda x: x[0], tbl_select.fetchall())
# Column names are saved in this variable
    template_data["cols"] = list(map(lambda x: x[0], cursor.description))
# primary key saved in this variable from fn arg
    template_data["pn"] = pk
# row with selected primary key value saved in this variable
    template_data["modrow"] = element_select.fetchall()
    return render_template('mod_form.html', **template_data)

#Used to receive values from html form if user level is highest
@app.route('/mod_tblxxx_entry', methods=['POST'])
def mod_tblxxx_entry():
    col = select_tbl_header(globvar_table_select)
    form_request = []
    query=''
    for x in range(len(col)):
        form_request.append(request.form[col[x]])
    form_request.append(request.form['modify'])
    for x in range(len(col)):
        query = query+col[x]+" = ?, "
    query_start = "UPDATE %s SET " %globvar_table_select
    query_end = query[:(len(query)-2)]
    sql_update_query = query_start+query_end+" WHERE pn = ?"
    g.db.execute(sql_update_query, form_request)
    g.db.commit()
    flash('New entry was successfully modified')
    return redirect(url_for('show_tblxxx_entries'))

# Check if login is valid google acc and if user has access to app
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
# Check if user has valid google email (check google responce)
    if check_token != True:
        flash('Invalid Email!')
        return redirect(url_for('login'))
    global globvar_cur_user_email
    globvar_cur_user_email = user_email
# adds '' marks to ever side of variables
    quoted_user = "'"+userid+"'"
    quoted_email = "'"+user_email+"'"
# accepting autherized users
    query_get_userid = "SELECT * FROM users"
    cursor = g.db.execute(query_get_userid)
    database_data["users+lvl+email+req"] = cursor.fetchall()
# All google_ids saved in this variable
    database_data["users"] = list(map(lambda x: x[0], database_data["users+lvl+email+req"]))
# All access levels are saved in this variable
    database_data["lvls"] = list(map(lambda x: x[1], database_data["users+lvl+email+req"]))
# All user email addresses are saved in this variable
    database_data["email"] = list(map(lambda x: x[2], database_data["users+lvl+email+req"]))
# Saved if user has sent autherization email or not
    database_data["req"] = list(map(lambda x: x[3], database_data["users+lvl+email+req"]))
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
# userid added to database, but usr_lvl will be added by admin via add_user.html
    if app_valid_user == "not in db":
        query_add_userinfo = "INSERT INTO users (google_id,usr_email,sent_auth_req_email) VALUES (%s,%s,'No')" \
            %(quoted_user,quoted_email)
        g.db.execute(query_add_userinfo)
        g.db.commit()
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
# If usr_lvl is 'null' in database
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
    message['from'] = config.MAIL_USERNAME
    message['subject'] = subject

    print("TEXT:")
    print(message)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(config.MAIL_USERNAME, config.MAIL_PASS)
    mailServer.sendmail(config.MAIL_USERNAME, config.MAIL_USERNAME, message.as_string())
    mailServer.close()

#If user is not yet in the database. Email is sent to the admin for user level access
@app.route('/awaiting_access')
def awaiting_access():
    if not session.get('awaiting_access'):
        return redirect(url_for('show_tblxxx_entries'))
# Check if email has already been sent
    sent_mail = ''
    query_check_mail_sent = 'SELECT sent_auth_req_email FROM users WHERE usr_email = \'%s\'' %globvar_cur_user_email
    cursor = g.db.execute(query_check_mail_sent)
    g.db.commit()
    sent_mail = cursor.fetchall()
    sent_mail = list(map(lambda x: x[0], sent_mail))
# Check if email was already sent or not. If yes dont send again
    if sent_mail == ['No']:
# Debug Message
        if config.DEBUG == True:
            print("No:In Here")
# Message to send
        msg = "New user "+globvar_cur_user_email+" has asked for access"
# Send email for admin to add user to database and set user level via SMTP
        send_message(config.MAIL_USERNAME,'New user access',msg)
# Change sent_auth_req_email to yes in db
        query_change_email_stat = 'UPDATE users SET sent_auth_req_email=\'Yes\' WHERE usr_email=\'%s\'' %globvar_cur_user_email
        g.db.execute(query_change_email_stat)
        g.db.commit()
        return render_template('awaiting_access.html')
    else:
# Debug Message
        if config.DEBUG == True:
            print("Yes:In Here")
        return render_template('awaiting_access.html')

# Displaying user in database and access levels in a table
@app.route('/user_management')
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
    if request.form['email'] == '':
        flash('Please select a user')
        return redirect(url_for('add_user_page'))
    if request.form['adduser'] == '':
        flash('Please select a permission level')
        return redirect(url_for('add_user_page'))
# Debug Message
    if config.DEBUG == True:
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
    flash('You were successfully logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
