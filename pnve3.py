# all the imports
import sqlite3
import os
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

#	cursor_partnumber = g.db.execute('select grp || '-' || substr('00000'||pn,-5,5) || '-' || ver from tbl1xx as partnumber')
	cursor = g.db.execute('select * from tbl1xx')
#	template_data["pn"] = cursor_partnumber_fetchall()
	template_data["rows"] = cursor.fetchall()
	template_data["cols"] = list(map(lambda x: x[0], cursor.description))
	return render_template('show_tblxxx_entries.html', **template_data)

@app.route('/addtbl1xx', methods=['POST'])
def add_tbl1xx_entry():
#    if not session.get('logged_in'):
#        abort(401)
	g.db.execute('insert into tbl1xx (grp, ver, value, param, desc, status, rohs, datasheet) values (?, ?, ?, ?, ?, ?, ?, ?)',
				[request.form['grp'], request.form['ver'], request.form['value'], request.form['param'], request.form['desc'], 					request.form['status'], request.form['rohs'], request.form['datasheet']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_tbl1xx_entries'))

if __name__ == '__main__':
	app.run()
