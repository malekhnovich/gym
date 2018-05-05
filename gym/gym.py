# all the imports
import os
import sqlite3
from pprint import pprint

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # app
app.config.from_object(__name__) # gym config coming from here
from .forms import classViewForm, editClassForm,deleteClassForm, deleteExerciseForm, addExerciseForm, AddEmployeeForm, EditFullTimeEmployeeForm, EditExternalEmployeeForm, DeleteEmployeeForm,SeeClassForm,JoinClassForm,checkClassesForm
from .gym import app

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

@app.route('/', methods = ["POST","GET"])
def get_classes():
    form = SeeClassForm()
    instructorId = form.instructorId.data
    classId = form.classId.data
    roomCap = form.roomCap.data
    db = get_db()
    c = db.cursor()
    print(form.classId)
    print(request.data)
    if request.method == "GET":
        cur =  db.execute( "select e.name as exerciseName,e.description,i.name as instructorName, c.classId as classId, c.buildingName, c.startTime, i.id as instructorId,i.name, r.capacity as roomCap, r.roomID from Instructor i join Class c on i.id = c.instructorID join  Exercise e on c.classId=e.id join Room r on r.roomID = c.roomID ")
        curexcercises = db.execute("select * from Exercise")
        # classes = cur.fetchall()
        classes = cur.fetchall()
        excercises = curexcercises.fetchall()
        return render_template("/sign_up.html", title = "sign up", form=form, classes=classes)






    cur =  db.execute("select  e.name as exerciseName,e.description,i.name as instructorName, c.classId as classId, c.buildingName, c.startTime, i.id as instructorId,i.name from Instructor i join Class c on i.id = c.instructorID join  Exercise e on c.classId=e.id")
    classes = cur.fetchall()

    #curClassSize = db.execute("select count(*) from Enrolled e where classId =?",None)
    #classSize = curClassSize.fetchone()[0]
   # print(classSize)
    #keep point what you want to refer to it as in templates
    return render_template("/sign_up.html", title="get classes", classes =  classes,form = form)

@app.route('/sign_up', methods = ["POST","GET"])
def sign_up():
    form = JoinClassForm()
    goBackForm = checkClassesForm()
    instructorId = form.instructorId.data
    classId = form.classId.data
    print("instructorid",instructorId,"class id:",classId)

    db = get_db()
    c = db.cursor()
    getEnrolledCur = db.execute("select count(*) from Enrolled as numberEnrolled where classId = ?", (classId,))
    getEnrolled = getEnrolledCur.fetchone()
    enrolled = getEnrolled[0]
    capacityCur = db.execute("select r.capacity as roomCap from Instructor i join Class c on i.id = c.instructorID join  Exercise e on c.classId=e.id join Room r on r.roomID = c.roomID where classId =?",(classId,))
    getCapacity = capacityCur.fetchone()
    capacity = getCapacity[0]
    #capacity = capacity[0]
    print(capacity)
    cur = db.execute(
        "select  e.name as exerciseName,e.description,i.name as instructorName,r.roomID as roomId, c.classId as classId, c.buildingName, c.startTime, i.id as instructorId,i.name from Instructor i join Class c on i.id = c.instructorID join  Exercise e on c.classId=e.id join room r on r.roomID = c.roomID where classId =?",(classId,))
    classes = cur.fetchall()

    # print("the capacity of this room is ",roomCap)
    print("the number of enrolled are",getEnrolled)
    if(enrolled>=capacity):
        recommendedCur = db.execute("select e.name as exerciseName, c.startTime, i.name as instructorName ,r.capacity, (select count(*) from Enrolled where classId = c.classId ) as enrolled from Class c, Exercise e, Instructor i, Room r where c.exerciseID = e.id and c.instructorID = i.id and c.buildingName = r.buildingName and c.roomID = r.roomID and r.capacity > enrolled order by enrolled asc limit 3")
        recommended = recommendedCur.fetchall()
        return render_template("/show_classes.html",title="no space",classes=classes, recommendedClasses = recommended ,capacity = capacity,enrolled=enrolled,backForm=goBackForm,form=form)
    else:
        nextEnrolled = enrolled+1
        db.execute("insert into Enrolled values(?,?)",(nextEnrolled,classId))
        db.commit()
        return render_template('/show_classes.html', title="main", classes=classes, capacity = capacity,enrolled =enrolled,form=form,backForm=goBackForm)
    # curMemberCount = db.execute("Select Count(*) from Member")
    # memberCount = curMemberCount.fetchall()
    # memberCount = memberCount[0][0]
    # print(memberCount)
    # classDetails = cur.fetchall()
    # print(classDetails)
    # curIncrease = db.execute("insert into Enrolled values (?, ?)", (None, memberCount))

    #return render_template("show_classes.html",classDetails=classDetails)


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
    cur = db.execute("insert into instructor values(?,?)", (None,name))
    if request.form['type']=="External":
        print('inserting external')
        cur = db.execute("insert into ExternalInstructor values (?,?,?,?)",(None,name,hours,hourlyWage))
    if request.form['type']=="FullTime":
        cur = db.execute("insert into FullTimeInstructor values (?,?,?)",(None,name,salary))
        print('inserting fulltime')

    db.commit()
    #if the insert was successfull, idk how you'd check for that in Flask
    return redirect(url_for('get_employees'))

@app.route('/edit_employee/<id>', methods=["POST", "GET"])
def edit_employee(id):
    formF = EditFullTimeEmployeeForm()
    formE = EditExternalEmployeeForm()

    if request.method == "GET":
        db = get_db()
        cur = db.execute("select * from Instructor i, FullTimeInstructor f where i.id = f.id and i.id = ?", (id))
        employeesF = cur.fetchall()
        cur2 = db.execute("select * from Instructor i, ExternalInstructor f where i.id = f.id and i.id = ?", (id))
        employeesE = cur2.fetchall()

        if len(employeesF) == 1: #we know it is a full timer
            return render_template("edit_fulltime_employee.html", form=formF, employee=employeesF[0])
        elif len(employeesE) == 1: #we know it is an external instructor
            return render_template("edit_external_employee.html", form=formE, employee=employeesE[0])
        else:
            return "Not an employee"

    elif request.method == "POST":
        if request.form['type'] == 'FullTime':
            name = request.form['name']
            salary = request.form['salary']
            db = get_db()
            cur =  db.execute( "update Instructor set name = ? where id = ?", (name,id))
            cur =  db.execute( "update FullTimeInstructor set salary = ? where id = ?", (salary,id))
            db.commit()
            return redirect(url_for('get_employees'))
        elif request.form['type'] == 'External':
            name = request.form['name']
            hoursTaught = request.form['hours']
            hourlyWage = request.form['hourlywage']
            db = get_db()
            cur =  db.execute( "update Instructor set name = ? where id = ?", (name,id))
            cur =  db.execute( "update ExternalInstructor set hoursTaught = ?, hourlywage = ? where id = ?", (hoursTaught,hourlyWage,id))
            db.commit()
            return redirect(url_for('get_employees'))
        else:
            return 'Invalid employee edit'

@app.route('/delete_employee', methods=["POST", "GET"])
def delete_employee():
    form = DeleteEmployeeForm()
    db = get_db()

    if request.method == "GET":
        cur =  db.execute( "select distinct i.id,i.name from Instructor i")
        employees = cur.fetchall()
        return render_template("delete_employee.html", title = "delete employee", form=form, employees=employees)

    id = form.id.data
    id = int(str(id)[:1])
    print(id)
    # curId = db.execute("Select ft.name from FullTimeInstructor ft where id = ?",(id,))

    cur = db.execute("Delete from Instructor where id = ?", (id,))
    ids = [r[0] for r in cur.fetchall()]
    print(ids)
    if id in ids:
        cur2 = db.execute("Delete from FullTimeInstructor where id = ?",(id,))

    else:
        cur2 =db.execute("Delete from ExternalInstructor where id = ?",(id,))
    db.commit()
    # employees = cur.fetchall()
    # # classes = cur.executemany(x)
    # keep point what you want to refer to it as in templates
    #return render_template("delete_employee.html", title = "delete employee", form=form)

    #if the insert was successfull, idk how you'd check for that in Flask
    return redirect(url_for('get_employees'))
@app.route('/view_exercises')
def view_exercises():
    db = get_db()
    curExercise = db.execute("Select e.name,e.description,e.id from exercise e")
    exercises = curExercise.fetchall()
    return render_template('view_exercises.html',exercises=exercises)

@app.route("/edit_exercises",methods = ['POST','GET'])
def editExercise():
    if request.form:
        pprint(request.form)
    exerciseName = request.form.get("exerciseName")
    exerciseDescription = request.form.get("exerciseDescription")
    exerciseId = request.form.get("exerciseId")
    db = get_db()
    cur = db.execute("Update Exercise set name=?,description=? where id = ?",(exerciseName,exerciseDescription,exerciseId))
    db.commit()
    return redirect('view_exercises')



@app.route('/add_exercises',methods=["POST", "GET"])
def add_exercises():
    form = addExerciseForm()
    if request.method == "GET":
        return render_template("add_exercises.html", title="add exercises", form=form)


    name = form.exerciseName.data
    description = form.exerciseDescription.data
    db = get_db()
    curAddExercise = db.execute("insert into exercise (name, description) VALUES (?,?)",(name,description))

    curAddExercise.fetchall()
    #curdeleteNone = db.execute("Delete from exercise where name =?",None)
    db.commit()
    return redirect('view_exercises')

@app.route('/delete_exercise',methods=["POST", "GET"])
def delete_exercise():
    form = deleteExerciseForm()
    db = get_db()

    if request.method == "GET":
        cur = db.execute("select distinct e.id,e.name,e.description from exercise e")
        exercises = cur.fetchall()
        return render_template("delete_exercise.html", title="delete exercise", form=form, exercises=exercises)

    id = request.form["id"]
    exerciseId = int(str(id)[:1])
    print("The id value is ",id)
    # curId = db.execute("Select ft.name from FullTimeInstructor ft where id = ?",(id,))

    # deleteExercise = db.execute("Delete from Exercise where id = ?", (id,))
    getClasses = db.execute("Select classId from Class where exerciseID = ?", (id,))
    classesToDelete =[r[0] for r in getClasses.fetchall()]
    print("classes to delete",classesToDelete)
    for i in classesToDelete:
        print("here")
        deleteClass = db.execute("Delete from Class where exerciseID = ?",(exerciseId,))
        deleteEnrolled = db.execute("Delete from Enrolled where classId = ?",(i,))
    deleteExercise = db.execute("Delete from exercise where id = ?",(exerciseId,))
    db.commit()
    return redirect(url_for('view_exercises'))

#where employees can view classes
@app.route("/class_view",methods = ['GET','POST'])
def class_view():
    db = get_db()
    form = classViewForm()
    curClasses = db.execute("select c.classId,c.instructorID,c.startTime,c.duration,c.exerciseID,r.buildingName,r.roomID, e.name as exerciseName,e.description,i.name as instructorName, c.classId as classId, c.buildingName, c.startTime,i.name, r.capacity as roomCap from Instructor i join Class c on i.id = c.instructorID join  Exercise e on c.exerciseID=e.id join Room r on r.roomID = c.roomID ")
# classes = cur.fetchall()
    classes = curClasses.fetchall()
    pprint("hELFLODOSFOSDOFSOFOSD")
    return render_template("class_view.html",classes=classes,form=form)


@app.route("/add_class", methods = ['POST','GET'])
def add_class():
    db = get_db()
    #pprint(request.form)

    lastInstructor = db.execute("select count(*) from Instructor as numberInstructor")
    lastInstructor = lastInstructor.fetchone()
    InstructorRow = lastInstructor[0]
    nextInstructorId = InstructorRow+1
    lastExercise = db.execute("select count(*) from Exercise as numberExercises")
    exerciseRow = lastExercise.fetchone()
    nextExcerciseId = exerciseRow[0]
    nextExcerciseId = nextExcerciseId+1
    exerciseName = request.form.get("exerciseName")
    exerciseId = db.execute("Select id from exercise where name =?",(exerciseName,))
    exerciseId= exerciseId.fetchone()
    exerciseId = exerciseId[0]
    instructorName = request.form.get("instructorName")
    print(instructorName)
    curInstructor = db.execute("Select id from instructor where name =?",(instructorName,))
    instructorID = curInstructor.fetchone()
    instructorID = instructorID[0]
    print("The instructor id is ",instructorID)
    startTime = request.form.get("startTime")
    duration=request.form.get("duration")
    exerciseDescription = request.form.get("exerciseDescription")
    newBuildingName  = request.form.get("newBuildingName")
    newRoomNumber  = request.form.get("newRoomNumber")
    newCapacity = request.form.get("newCapacity")
    newClassDuration = request.form.get("newClassDuration")

    lastClass = db.execute("select count(*) from Class as numberInstructor")

    cur = db.execute("insert into Class (classId,instructorID,startTime,duration, exerciseID, buildingName,roomID) Values(?,?,?,?,?,?,?)",(None,instructorID,startTime,newClassDuration,exerciseId,newBuildingName,newRoomNumber))
    cur2 =db.execute("insert into Room(buildingName,roomID, capacity) Values(?,?,?)",(newBuildingName,newRoomNumber, newCapacity))
    #TODO:make add take in exercise rather than id
    db.commit()
    return redirect (url_for('class_view'))

@app.route("/edit_class",methods = ['POST','GET'])
def editClass():
    #pprint("XASAFLKDANFSKFNAKKANSNDSNADSLKADSK")
    if request.form:
        pprint(request.form)
    classId = request.form.get('classId')
    newStartTime = request.form.get('newStartTime')
    if newStartTime==None:
        oldStartTime = request.form.get('oldStartTime')
        newStartTime = oldStartTime
    newClassDuration  =request.form.get('newClassDuration')
    if newClassDuration==None:
        oldClassDuration = request.form.get('oldClassDuration')
        newClassDuration= oldClassDuration

    newBuildingName = request.form.get("newBuildingName")
    oldBuildingName = request.form.get("oldBuildingName")
    if newBuildingName==None:
        oldBuildingName = request.form.get("oldBuildingName")
        newBuildingName = oldBuildingName

    newRoomNumber = request.form.get("newRoomNumber")
    oldRoomNumber = request.form.get("oldRoomNumber")
    if newRoomNumber==None:
        pprint("ejpiapiajpapjpsdjpdsjasd")
        oldRoomNumber=request.form.get("oldRoomNumber")
        newRoomNumber=oldRoomNumber
    pprint(newRoomNumber)
    newInstructorName = request.form.get("newInstructorName")
    if newInstructorName==None:
        oldInstructorName=request.form.get("oldInstructorName")
        newInstructorName=oldInstructorName
    newClassDuration = newClassDuration
    newExerciseDescription=request.form.get("newExerciseDescription")
    if newExerciseDescription==None:
        newExerciseDescription=request.form.get("oldExerciseDescription")
        newExerciseDescription=oldExerciseDescription
    newExerciseName=request.form.get("newExerciseName")
    if newExerciseName==None:
        oldExerciseName=request.form.get("oldExerciseName")
        newExerciseName=oldExerciseName
    exerciseId = request.form.get("exerciseId")
    instructorId = request.form.get('instructorId')
    print("The value of id is ",instructorId)
    if request.method =="GET" or request.method=="POST":
        print("here")
        db = get_db()
        cur = db.execute("update Class set startTime = ?, instructorID =?, duration =?,buildingName =?,roomID =? where classId = ?",(newStartTime,instructorId,newClassDuration,newBuildingName,newRoomNumber,classId))
        cur2 =db.execute("update Instructor set name = ? where id = ?",(newInstructorName,instructorId))
        cur3 = db.execute("update Room set roomID=?,buildingName=? where roomId = ? and buildingName = ?",(newRoomNumber,newBuildingName,oldRoomNumber,oldBuildingName))
        cur4 = db.execute("update Exercise set name=?,description=? where id = ?",(newExerciseName, newExerciseDescription,exerciseId))
        db.commit()
        return redirect("/class_view")
    else:
        return "invalid attempt at editing"




@app.route('/delete_class',methods = ["POST","GET"])
def delete_class():
    pprint(request.form)
    db = get_db()
    cur = db.execute("select c.classId,c.instructorID,c.startTime,c.duration,c.exerciseID,c.buildingName,c.roomID, e.name as exerciseName,e.description,i.name as instructorName, c.classId as classId, c.buildingName, c.startTime, i.id as instructorId,i.name, r.capacity as roomCap, r.roomID from Instructor i join Class c on i.id = c.instructorID join  Exercise e on c.classId=e.id join Room r on r.roomID = c.roomID")
    DeleteClass = cur.fetchall()
    classId = request.form.get('classId')
    instructorId = request.form.get('instructorId')
    #id=int(str(id)[:1])
    print("id value is",classId)

    cur = db.execute("Delete from Class  where classId = ? and instructorId = ?",(classId,instructorId))
    db.commit()
    return redirect(('/class_view'))

@app.route('/payroll')
def view_payroll():
    db = get_db()

    # 10% federal tax, 5% state tax and 3% for other taxes
    externalMonthlyTaxCur = db.execute("Select distinct ei.id,ei.name,ei.hoursTaught,ei.hourlywage,((ei.hourlywage*ei.hoursTaught)*(0.10)+(ei.hourlywage*ei.hoursTaught)*(0.05)+(ei.hourlywage*ei.hoursTaught)*(0.03)) as tax, ei.hourlywage*ei.hoursTaught as salary from ExternalInstructor ei")
    eemTax = externalMonthlyTaxCur.fetchall()
    # curYearly = db.execute("Select ft.id, ft.salary*12 from FullTimeInstructor ft")
    curMonthlyTax = db.execute("Select distinct ft.id,ft.name,ft.salary, (((ft.salary*(.10))+(ft.salary*(.05))+(ft.salary*(0.03)))) as tax from FullTimeInstructor ft")
    femTax = curMonthlyTax.fetchall()
    #fullEmpMonthlyTax = curMonthlyTax.fetchall()
    print(femTax)
    #print(externalEmpMonthly[0][0])
    # exYearlySalary = list()
    # exMonthlyTax = list()
    # fullYearlySalary = list()
    # fullMonthlyTax = list()
    # for x in range(len(externalEmpMonthly)):
    #     salary = externalEmpMonthly[x][0]
    #     yearly_salary = salary*12
    #     exYearlySalary.append(yearly_salary)
    #     monthlyTax = salary*(.10)+salary*(.05)+salary*(.03)
    #     exMonthlyTax.append(monthlyTax)
    # for x in range(len(fullEmpMonthly)):
    #     salary = fullEmpMonthly[x][0]
    #     yearly_salary = salary*12
    #     fullYearlySalary.append(yearly_salary)
    #     monthlyTax = salary*(.10)+salary*(.05)+salary*(.03)
    #     print(monthlyTax)
    #     fullMonthlyTax.append(monthlyTax)

#    print(fullEmpMonthlyTax)
    # print("yearly fulltime salary is")
    # print(yearlyFullTime)

    #print(yearlyFullTime[0][0])
    # print("yearly salary %(yearlyFullTime)d"%{yearlyFullTime})
    return render_template("view_payroll.html",extEmpMonthlyTax = eemTax,fullEmpMonthlyTax=femTax)




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
