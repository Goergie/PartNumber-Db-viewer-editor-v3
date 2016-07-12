# all the imports
import sqlite3
import os
import json
import httplib2
import base64
import jwt

from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify

from contextlib import closing

from oauth2client import client, crypt
from apiclient.discovery import build

# configuration
cwd = os.getcwd()
rel_path = os.path.join(cwd, 'tmp/pnve3.db')
DATABASE_PATH = rel_path
DEBUG = True
SECRET_KEY = 'dev_key'
USERNAME_USER_LEVEL = 'guest'
PASSWORD_USER_LEVEL = 'userjelszo'
USERNAME_ENGINEER_LEVEL = 'admin'
PASSWORD_ENGINEER_LEVEL = 'adminjelszo'
USERNAME_ADMIN_LEVEL = 'sadmin'
PASSWORD_ADMIN_LEVEL = 'superadmin'
ADMIN_EMAIL = 'apnvev@gmail.com'

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)

globvar_table_select = 'tbl1xx'

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
          print ("inside here")
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

@app.route('/verify', methods=['POST'])
def verify():
    app_valid_user = 0
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
    quoted_user = "'"+userid+"'"
# accepting autherized users
    query_get_userid = "SELECT * FROM users"
    cursor = g.db.execute(query_get_userid)
    database_data["users+lvl"] = cursor.fetchall()
    database_data["users"] = list(map(lambda x: x[0], database_data["users+lvl"]))
    database_data["lvls"] = list(map(lambda x: x[1], database_data["users+lvl"]))
    print("test",userid)
    for user in database_data["users"]:
        print ("user:",user)
        if user == userid:
            query_check_lvl = "SELECT usr_lvl FROM users WHERE google_id = %s" %quoted_user
            get_lvl = g.db.execute(query_check_lvl)
            get_lvl = get_lvl.fetchall()
            get_lvl = list(map(lambda x: x[0], get_lvl))
            print(get_lvl)
            if get_lvl != [None]:
                app_valid_user = 2
                print("Logged in User:",user)
                break
            else:
                app_valid_user = 1
            #user is already in database
    if app_valid_user == 0:
        query_add_userid = "INSERT INTO users (google_id) VALUES (%s)" %quoted_user
        g.db.execute(query_add_userid)
        g.db.commit()
        #userid added to database, but usr_lvl will be added by admin
    query_select_user_level = "SELECT usr_lvl FROM users WHERE google_id = %s" %quoted_user
    selected_users_access_lvl = g.db.execute(query_select_user_level)
    database_data["lvl"] = list(map(lambda x: x[0], selected_users_access_lvl))
    if app_valid_user == 2:
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
    else:
        print( "Request access!")
        session['awaiting_access'] = True
        return redirect(url_for('awaiting_access'))
#    return redirect(url_for('show_tblxxx_entries'))

#If user is not yet in the database. Email is sent to the admin for user level access
@app.route('/awaiting_access')
def awaiting_access():
    session.pop('awaiting_access', None)
    #send email for admin to add user to database and set user level
    return render_template('awaiting_access.html')

@app.route('/add_user_page')
def add_user_page():
    if not session.get('logged_in_admin'):
        return redirect(url_for('show_tblxxx_entries'))
    database_data = {}
    query_get_userid = "SELECT google_id FROM users"
    cursor = g.db.execute(query_get_userid)
    database_data["users_tmp"] = cursor.fetchall()
    database_data["users"] = list(map(lambda x: x[0], database_data["users_tmp"]))
    return render_template('add_user.html', **database_data)

@app.route('/add_user',methods=['POST'])
def add_user():
    user_id = "'"+request.form['user_id']+"'"
    print(user_id)
    user_lvl = int(request.form['adduser'])
    print("value:",user_lvl)
    query_add_user = "UPDATE users SET usr_lvl = ? WHERE google_id = ?"
    g.db.execute(query_add_user, [user_lvl, user_id])
    g.db.commit()
    flash('User rights level successfully changed')
    return redirect(url_for('show_tblxxx_entries'))

#If logout button is pressed then user session is popped and filled with none
@app.route('/logout')
def logout():
    session.pop('logged_in_guest', None)
    session.pop('logged_in_engineer', None)
    session.pop('logged_in_admin', None)
    flash('You were logged out')
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run()
