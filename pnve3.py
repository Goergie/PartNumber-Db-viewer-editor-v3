# all the imports
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
cwd = os.getcwd()
rel_path = os.path.join(cwd, 'tmp/pnve3.db')
DATABASE = rel_path
DEBUG = True
SECRET_KEY = 'dev_key'
USERNAME = 'admin'
PASSWORD = 'jelszo'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

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
def show_entries():
	cursor = g.db.execute('select * from resistor order by pn desc')
	cursor_cols_db = g.db.execute('pragma table_info(resistor)')
	db_rows = cursor.fetchall()
	print db_rows[0]
	cols_db = cursor_cols_db.fetchall()
	print cols_db[0]
	return render_template('show_db_entries.html', db_rows=db_rows, cols_db=cols_db)

if __name__ == '__main__':
    app.run()
