# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # app
app.config.from_object(__name__) # gym config coming from here
from forms import AddEmployeeForm,DeleteEmployeeForm
from gym import app

app.config.update(dict(
    DATABASE="gym.db",
    SECRET_KEY='admin',
    USERNAME='admin',
    PASSWORD='password'
))
#not using env variables for this
#app.config.from_envvar('GYM_SETTINGS', silent=True)


def connect_db():
    """connects to the specified database"""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#___________routes______________________

@app.route('/')
def get_classes():
    db = get_db()
    c = db.cursor()
    cur =  db.execute( "select distinct c.startTime,c.duration, e.name,e.description  from Class c join Exercise e join Instructor i")
    classes = cur.fetchall()
    # classes = cur.executemany(x)

    #keep point what you want to refer to it as in templates
    return render_template("show_classes.html", classes =  classes)


@app.route('/show_employees')
def get_employees():
    db = get_db()
    c = db.cursor()
    cur =  db.execute( "select distinct i.id,i.name from Instructor i")
    employees = cur.fetchall()
    # classes = cur.executemany(x)

    #keep point what you want to refer to it as in templates
    return render_template("show_employees.html", employees =  employees)

@app.route('/add_employee')
def add_employee():
    form = AddEmployeeForm()
    # name= request.form['name']
    # type  = request.form['job_status']
    db = get_db()
    # cur = db.execute("insert into instructor (?,?) values(id,name)")
    return render_template("add_employee.html",title="add employee",form=form)


@app.route('/delete_employee')
def delete_employee():
    db = get_db()
    form = DeleteEmployeeForm()
    # TODO:must remember to remove instructor from additional table (external or fulltime)
    # cur = db.execute("Delete from instructor where id = ?",id)
    # employees = cur.fetchall()
    # # classes = cur.executemany(x)
    # keep point what you want to refer to it as in templates
    return render_template("delete_employee.html", title = "delete employee", form=form)




    # @app.route('/exercise_signup',methods= ['POST'])
# def sign_up():
#     db = get_db()
#     cur = db.execute('insert into Class(instructorID, startTime,duration) values (?,?,?)',
#                [request.form['instructorID'],request.form['startTime'],request.form['duration']])


# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)

#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))