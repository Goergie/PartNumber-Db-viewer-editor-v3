# all the imports
import sqlite3
import os
from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
cwd = os.getcwd()
rel_path = os.path.join(cwd, 'tmp/pnve3.db')
DATABASE_PATH = rel_path
DEBUG = True
SECRET_KEY = 'dev_key'
USERNAME = 'admin'
PASSWORD = 'jelszo'

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)

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

@app.route('/')
def show_tbl1xx_entries():
    template_data = {}
    #cursor_partnumber = g.db.execute('select grp || '-' || substr('00000'||pn,-5,5) || '-' || ver from tbl1xx as partnumber')
    cursor = g.db.execute('SELECT * FROM tbl1xx')
    get_tbl1xx_entry_id = g.db.execute('SELECT pn FROM tbl1xx')
    #template_data["pn"] = cursor_partnumber_fetchall()
    query_for_tbl_select = "SELECT name FROM sqlite_master WHERE name LIKE 'tbl%'"
    tbl_select = g.db.execute(query_for_tbl_select)
    template_data["rows"] = cursor.fetchall()
    template_data["tbls"] = map(lambda x: x[0], tbl_select.fetchall())
    template_data["cols"] = list(map(lambda x: x[0], cursor.description))
    template_data["pn_id"] = map(lambda x: x[0], get_tbl1xx_entry_id.fetchall())
    return render_template('show_tblxxx_entries.html', **template_data)

@app.route('/addtbl1xx', methods=['POST'])
def add_tbl1xx_entry():
#    if not session.get('logged_in'):
#        abort(401)
	g.db.execute('INSERT INTO tbl1xx (grp, ver, value, param, desc, status, rohs, datasheet) \
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        [request.form['grp'], request.form['ver'], request.form['value'], request.form['param'], request.form['desc'],
        request.form['status'], request.form['rohs'], request.form['datasheet']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_tbl1xx_entries'))

@app.route('/deltbl1xx', methods=['POST'])
def del_tbl1xx_entry():
#   if not session.get('logged_in'):
#       abort(401)
#    g.db.execute('DELETE FROM tbl1xx WHERE pn=?,)
#	g.db.commit()
    flash('Entry was successfully deleted')
    return redirect(url_for('show_tbl1xx_entries'))

@app.route('/mod_tbl1xx_entry')
def mod_tbl1xx_entry():
#    if not session.get('logged_in'):
#        abort(401)
    template_data = {}
    select_cursor = g.db.execute('select * from tbl1xx')
#    cursor = g.db.execute('Update tbl1xx set grp = ?, ver = ?, value = ?, param = ?, desc = ?, status = ?, rohs = ?, \
#         datasheet = ?, where pn = ?',[request.form['grp'], request.form['ver'], request.form['value'],
#         request.form['param'], request.form['desc'],request.form['status'], request.form['rohs'],
#         request.form['datasheet']],request.form['pn'])
    template_data["col_name"] = list(map(lambda x: x[0], select_cursor.description))
#    g.db.commit()
    return render_template('mod_form.html', **template_data)

if __name__ == '__main__':
	app.run()
