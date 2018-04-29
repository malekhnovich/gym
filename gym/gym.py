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

@app.route('/add_employee', methods=["POST", "GET"])
def add_employee():
    form = AddEmployeeForm()

    if request.method == "GET":
        return render_template("add_employee.html",title="add employee",form=form)

    name = form.name.data
    type  = form.type.data
    salary = form.salary.data
    hourlyWage = form.hourlyWage.data
    hours = form.hours.data

    db = get_db()
    cur = db.execute("insert into instructor values(?,?)", (id,name))
    if type=="External":
        cur = db.execute("insert into ExternalInstructor values (?,?,?,?)",(id,name,hours,hourlyWage))
    if type=="FullTime":
        cur = db.execute("insert into FullTimeInstructor values (?,?,?)",(id,name,salary))

    #if the insert was successfull, idk how you'd check for that in Flask
    return "New Employee Created"

@app.route('/delete_employee', methods=["POST", "GET"])
def delete_employee():
    form = DeleteEmployeeForm()
    db = get_db()

    if request.method == "GET":
        cur =  db.execute( "select distinct i.id,i.name from Instructor i")
        employees = cur.fetchall()
        return render_template("delete_employee.html", title = "delete employee", form=form, employees=employees)

    id = form.id.data
    #return id #for debugging

    # TODO:must remember to remove instructor from additional table (external or fulltime)
    cur = db.execute("Delete from instructor where id = ?",id)
    # employees = cur.fetchall()
    # # classes = cur.executemany(x)
    # keep point what you want to refer to it as in templates
    #return render_template("delete_employee.html", title = "delete employee", form=form)

    #if the insert was successfull, idk how you'd check for that in Flask
    return "Employee Deleted"

@app.route('/payroll')
def view_payroll():
    db = get_db()
    # 10% federal tax, 5% state tax and 3% for other taxes
    cur = db.execute("Select * from FullTimeInstructor")
    fulltimeEmp = cur.fetchall()
    cur2 = db.execute("Select * from ExternalInstructor")
    externalEmp = cur2.fetchall()
    curMonthly = db.execute("Select ft.salary from FullTimeInstructor ft")
    monthlySalaries = curMonthly.fetchall()
    curPT = db.execute("Select (et.hourlywage*et.hoursTaught)  from ExternalInstructor et")
    externalEmpMonthly = curPT.fetchall()
    # curYearly = db.execute("Select ft.id, ft.salary*12 from FullTimeInstructor ft")
    curMonthly = db.execute("Select ft.salary from FullTimeInstructor ft")
    fullEmpMonthly = curMonthly.fetchall()
    #print(externalEmpMonthly[0][0])
    print("external monthly salary is")
    exYearlySalary = list()
    exMonthlyTax = list()
    fullYearlySalary = list()
    fullMonthlyTax = list()
    for x in range(len(externalEmpMonthly)):
        salary = externalEmpMonthly[x][0]
        yearly_salary = salary*12
        exYearlySalary.append(yearly_salary)
        monthlyTax = salary*(.10)+salary*(.05)+salary*(.03)
        exMonthlyTax.append(monthlyTax)
    for x in range(len(fullEmpMonthly)):
        salary = fullEmpMonthly[x][0]
        yearly_salary = salary*12
        fullYearlySalary.append(yearly_salary)
        yearlyTax = salary*(.10)+salary*(.05)+salary*(.03)
        fullMonthlyTax.append(yearlyTax)

    # print("yearly fulltime salary is")
    # print(yearlyFullTime)

    #print(yearlyFullTime[0][0])
    # print("yearly salary %(yearlyFullTime)d"%{yearlyFullTime})
    return render_template("view_payroll.html",fulltimeEmp=fulltimeEmp,externalEmp=externalEmp,

                           externalEmpMonthly = externalEmpMonthly,monthlySalaries = monthlySalaries,
                           exYearlyTax = exMonthlyTax, exYearlySalary= exYearlySalary,
                           fullYearlyTax=fullMonthlyTax,fullYearlySalary=fullYearlySalary)




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
