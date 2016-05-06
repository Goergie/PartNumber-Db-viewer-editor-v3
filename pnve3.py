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
		with app.open_resource('pn_db_schema.sql', mode='r') as f:
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
	cursor = g.db.execute('select * from resistors order by pn desc')
	rowfromdb = [dict(pn=rowfromdb[0], value=rowfromdb[1], param=rowfromdb[2], desc=rowfromdb[3],
		status=rowfromdb[4], rohs=rowfromdb[5], datasheet=rowfromdb[6])
			 for rowfromdb in cursor.fetchall()]
#	while rowfromdb is not None:
#		print pn, value, param,
#		rowfromdb=cursor.fetchone()
	return render_template('show_db_entries.html', rowfromdb=rowfromdb)

if __name__ == '__main__':
    app.run()
