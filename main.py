from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from MySQLdb import IntegrityError
from flask import send_file
import base64
import io 
import smtplib

app = Flask(__name__)

senderEmail = "sheikhtoocool@gmail.com"
appPassword = "ovquggubuadgkqqc"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lmsdb'
app.secret_key = 'theKey'
mysql = MySQL(app)

@app.route('/')
def renderRoleSelectionPage():
    return render_template('roleSelectionPage.html')

@app.route('/admin_dashboard')
def renderAdminDashboardPage():
    return render_template('adminDashboard.html')

@app.route('/student_dashboard')
def renderStudentDashboardPage():
    return render_template('studentDashboard.html', data = session['user'])

@app.route('/teacher_dashboard')
def renderTeacherDashboardPage():
    return render_template('teacherDashboard.html', data = session['user'])

@app.route('/admin_login')
def renderAdminLoginPage():
    return render_template('adminLogin.html')

@app.route('/teacher_login')
def renderTeacherLoginPage():
    return render_template('teacherLogin.html')

@app.route('/student_login')
def renderStudentLoginPage():
    return render_template('studentLogin.html')

@app.route('/academicAdvisor_login')
def renderAcademicAdvisorLoginPage():
    return render_template('advisorLogin.html')

@app.route('/hod_login')
def renderHODLoginPage():
    return render_template('hodLogin.html')

@app.route('/collegeAgent_login')
def renderCollegeAgentLoginPage():
    return render_template('collegeAgentLogin.html')

@app.route('/admin_addNewCourse')
def renderAdminAddNewCoursePage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * from teachers')
    data=cursor.fetchall()
    cursor.close()
    return render_template('admin_addNewCourse.html', teachers = data)

@app.route('/admin_addNewClass')
def renderAdminAddNewClassPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * from teachers')
    data=cursor.fetchall()
    cursor.execute('SELECT * from courses')
    data2=cursor.fetchall()
    cursor.close()
    return render_template('admin_addNewClass.html', teachers = data, courses = data2)

@app.route('/admin_addNewStudent')
def renderAdminAddNewStudentPage():
    return render_template('admin_addNewStudent.html')

@app.route('/admin_addNewTeacher')
def renderAdminAddNewTeacherPage():
    return render_template('admin_addNewTeacher.html')

@app.route('/authenticateAdmin', methods=['GET', 'POST'])
def authenticateAdmin():
    if request.method == 'POST':
        email = request.form['adminEmail']
        password = request.form['adminPassword']

        # Check credentials in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM adminRecords WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Store user in session
            session['user'] = user
            return render_template('adminDashboard.html')
        else:
            msg = 'Incorrect email or password. Please try again New data.'

    return render_template('adminLogin.html', msg = msg)

@app.route('/authenticateTeacher', methods=['GET', 'POST'])
def authenticateTeacher():
    if request.method == 'POST':
        email = request.form['teacherEmail']
        password = request.form['teacherPassword']

        # Check credentials in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teachers WHERE teacherEmail = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Store user in session
            session['user'] = user
            return render_template('teacherDashboard.html', data = user)
        else:
            msg = 'Incorrect email or password. Please try again.'

    return render_template('teacherLogin.html', msg = msg)

@app.route('/authenticateStudent', methods=['GET', 'POST'])
def authenticateStudent():
    if request.method == 'POST':
        email = request.form['studentEmail']
        password = request.form['studentPassword']

        # Check credentials in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE studentEmail = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Store user in session
            session['user'] = user
            return render_template('studentDashboard.html', data = user)
        else:
            msg = 'Incorrect email or password. Please try again.'

    return render_template('studentLogin.html', msg = msg)

@app.route('/addNewCourseToDB', methods=['POST'])
def addNewCourseToDB():
    try:
        # Get form data
        courseCode = request.form['courseCode']
        courseTitle = request.form['courseTitle']
        creditHours = request.form['creditHours']
        className = request.form['className']
        teacherName = request.form['teacherName']

        # Insert data into the 'courses' table
        dbb = MySQLdb.connect(host="localhost", user="root", passwd="", db="lmsdb")
        curb = dbb.cursor()
        curb.execute("""
            INSERT INTO courses (courseCode, courseTitle, creditHours, class, teacherName)
            VALUES (%s, %s, %s, %s, %s)
        """, (courseCode, courseTitle, creditHours, className, teacherName))
        dbb.commit()
        curb.close()

        return redirect(url_for('renderAdminAddNewCoursePage'))

    except IntegrityError:
        # Handle duplicate key violation
        error_message = "Course with code '{}' already exists.".format(courseCode)
        return render_template('admin_addNewCourse.html', error=error_message)
    
@app.route('/addNewStudentToDB', methods=['POST'])
def addNewStudentToDB():
    try:
        # Get form data
        studentID = request.form['studentId']
        studentName = request.form['studentName']
        gpa = request.form['gpa']
        studentEmail = request.form['studentEmail']
        studentProgram=request.form['studentProgram']

        # Insert data into the 'students' table
        dbb = MySQLdb.connect(host="localhost", user="root", passwd="", db="lmsdb")
        curb = dbb.cursor()
        curb.execute("""
            INSERT INTO students (studentID,studentName,gpa,studentEmail,studentProgram,password)
            VALUES (%s, %s, %s, %s,%s,%s)
        """, (studentID,studentName,gpa,studentEmail,studentProgram,"12345"))
        dbb.commit()
        curb.close()

        return redirect(url_for('renderAdminAddNewStudentPage'))

    except IntegrityError:
        # Handle duplicate key violation
        error_message = "Student with ID '{}' already exists.".format(studentID)
        return render_template('admin_addNewStudent.html', error=error_message)

@app.route('/addNewTeacherToDB', methods=['POST'])
def addNewTeacherToDB():
    try:
        # Get form data
        teacherID = request.form['teacherId']
        teacherName = request.form['teacherName']
        teacherEmail = request.form['teacherEmail']
        specialization = request.form['specialization']

        # Insert data into the 'teachers' table
        dbb = MySQLdb.connect(host="localhost", user="root", passwd="", db="lmsdb")
        curb = dbb.cursor()
        curb.execute("""
            INSERT INTO teachers (teacherID,teacherName,specialization,teacherEmail,password)
            VALUES (%s, %s, %s, %s,%s)
        """, (teacherID,teacherName,specialization,teacherEmail,"12345"))
        dbb.commit()
        curb.close()

        return redirect(url_for('renderAdminAddNewTeacherPage'))

    except IntegrityError:
        # Handle duplicate key violation
        error_message = "Teacher with ID '{}' already exists.".format(teacherID)
        return render_template('admin_addNewTeacher.html', error=error_message)

@app.route('/coursesListing')
def renderAdminShowAllCoursesPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM courses')
    data=cursor.fetchall()
    cursor.close()
    return render_template('admin_showAllCourses.html', courses = data)

@app.route('/studentsListing')
def renderAdminShowAllStudentsPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM students')
    data=cursor.fetchall()
    cursor.close()
    return render_template('admin_showAllStudents.html', students = data)

@app.route('/teachersListing')
def renderAdminShowAllTeachersPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM teachers')
    data=cursor.fetchall()
    cursor.close()
    return render_template('admin_showAllTeachers.html', teachers = data)

@app.route('/classesListing')
def renderAdminShowAllClassesPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM classRecords')
    data = cursor.fetchall()
    cursor.close()

    # Group students by class
    students_by_class = {}
    for student in data:
        student_class = student['class']  # Assuming 'studentProgram' is the field representing the class
        if student_class not in students_by_class:
            students_by_class[student_class] = []
        students_by_class[student_class].append(student)

    return render_template('admin_showAllClasses.html', students_by_class=students_by_class)

# Route for the deleting a course
@app.route('/deleteCourses/<string:course_id>', methods=['POST'])
def delete_course(course_id):
    dbb = MySQLdb.connect(host="localhost", 
       user="root", 
       passwd="", 
       db="lmsdb") 
    curb = dbb.cursor()
    curb.execute ("delete from courses where courseCode = %s", (course_id,))
    dbb.commit()
    curb.close()
    
    return redirect('/coursesListing')

# Route for the updating a course
@app.route('/updateCourses/<string:course_id>', methods=['POST'])
def update_course(course_id):
    courseCode = request.form['courseCode']
    courseTitle = request.form['courseTitle']
    creditHours = request.form['creditHours']
    className = request.form['class']
    teacherName = request.form['teacherName']
    dbb = MySQLdb.connect(host="localhost", 
    user="root", 
    passwd="", 
    db="lmsdb") 
    curb = dbb.cursor()
    curb.execute("UPDATE courses SET courseCode = %s, courseTitle = %s, creditHours = %s, class = %s, teacherName = %s WHERE courseCode = %s", (courseCode, courseTitle, creditHours, className, teacherName, course_id,))
    dbb.commit()
    curb.close()

    return redirect('/coursesListing')

# Route for the deleting a student
@app.route('/deleteStudents/<string:student_id>', methods=['POST'])
def delete_student(student_id):
    dbb = MySQLdb.connect(host="localhost", 
       user="root", 
       passwd="", 
       db="lmsdb") 
    curb = dbb.cursor()
    curb.execute ("delete from students where studentID = %s", (student_id,))
    dbb.commit()
    curb.close()
    
    return redirect('/studentsListing')

# Route for the updating a student
@app.route('/updateStudents/<string:student_id>', methods=['POST'])
def update_student(student_id):
    studentID = request.form['studentID']
    gpa = request.form['gpa']
    studentName = request.form['studentName']
    studentEmail = request.form['studentEmail']
    studentProgram = request.form['studentProgram']
    dbb = MySQLdb.connect(host="localhost", 
    user="root", 
    passwd="", 
    db="lmsdb") 
    curb = dbb.cursor()
    curb.execute("UPDATE students SET studentID = %s, studentName = %s, gpa = %s, studentEmail = %s, studentProgram = %s WHERE studentID = %s", (studentID, studentName, gpa, studentEmail, studentProgram, student_id,))
    dbb.commit()
    curb.close()

    return redirect('/studentsListing')

# Route for the deleting a teacher
@app.route('/deleteTeachers/<string:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id):
    dbb = MySQLdb.connect(host="localhost", 
       user="root", 
       passwd="", 
       db="lmsdb") 
    curb = dbb.cursor()
    curb.execute ("delete from teachers where teacherID = %s", (teacher_id,))
    dbb.commit()
    curb.close()
    
    return redirect('/teachersListing')

# Route for the updating a teacher
@app.route('/updateTeachers/<string:teacher_id>', methods=['POST'])
def update_teacher(teacher_id):
    teacherID = request.form['teacherID']
    teacherName = request.form['teacherName']
    teacherEmail = request.form['teacherEmail']
    specialization = request.form['specialization']
    dbb = MySQLdb.connect(host="localhost", 
    user="root", 
    passwd="", 
    db="lmsdb") 
    curb = dbb.cursor()
    curb.execute("UPDATE teachers SET teacherID = %s, teacherName = %s, teacherEmail = %s, specialization = %s WHERE teacherID = %s", (teacherID, teacherName, teacherEmail, specialization, teacher_id,))
    dbb.commit()
    curb.close()

    return redirect('/teachersListing')

@app.route('/searchTheStudent', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the search input value
        search_input = request.form.get('search_input')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from students where studentID = %s", (search_input,))
        student =cursor.fetchone()
        if student:
            cursor.execute('SELECT * from teachers')
            data=cursor.fetchall()
            cursor.execute('SELECT * from courses')
            data2=cursor.fetchall()
            cursor.close()
            return render_template('admin_addNewClass.html', teachers = data, courses = data2, student=student)


    return render_template('admin_addNewClass.html', msg = "Student Not Found!")

@app.route('/addNewClassToDB', methods=['POST'])
def addNewClassToDB():
     # Get form data
        studentId = request.form['studentId']
        studentName = request.form['studentName']
        courseTitle = request.form['courseTitle']
        creditHours = request.form['creditHours']
        className = request.form['className']
        teacherName = request.form['teacherName']

        # Insert data into the 'students' table
        dbb = MySQLdb.connect(host="localhost", user="root", passwd="", db="lmsdb")
        curb = dbb.cursor()
        curb.execute("""
            INSERT INTO classRecords (studentID,studentName,courseTitle,creditHours,class,teacher,allowedLeaves)
            VALUES (%s, %s, %s, %s,%s, %s, %s)
        """, (studentId,studentName,courseTitle,creditHours,className,teacherName,10))
        dbb.commit()
        curb.close()

        return redirect(url_for('renderAdminAddNewClassPage'))

@app.route('/classesListingStudent')
def renderStudentShowAllClassesPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = session['user']
    studentid = data['studentID']
    cursor.execute('SELECT * FROM classRecords where studentid = %s', (studentid,))
    data = cursor.fetchall()
    cursor.close()

    # Group students by class
    students_by_class = {}
    for student in data:
        student_class = student['class']  # Assuming 'studentProgram' is the field representing the class
        if student_class not in students_by_class:
            students_by_class[student_class] = []
        students_by_class[student_class].append(student)

    return render_template('student_showAllClasses.html', students_by_class=students_by_class)

##################################################################################################################
@app.route('/logout')
def logout():
    # Clear the session upon logout
    session.pop('user', None)    
    
    return redirect('/')

@app.route('/authenticateHod', methods=['GET', 'POST'])
def authenticateHod():
    if request.method == 'POST':
        email = request.form['hodEmail']
        password = request.form['hodPassword']

        # Check credentials in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hodRecords WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Store user in session
            session['user'] = user
            return render_template('hodDashboard.html')
        else:
            msg = 'Incorrect email or password. Please try again New data.'

    return render_template('hodLogin.html', msg = msg)

@app.route('/authenticateAdvisor', methods=['GET', 'POST'])
def authenticateAdvisor():
    if request.method == 'POST':
        email = request.form['advisorEmail']
        password = request.form['advisorPassword']

        # Check credentials in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM advisorrecords WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Store user in session
            session['user'] = user
            return render_template('advisorDashboard.html')
        else:
            msg = 'Incorrect email or password. Please try again New data.'

    return render_template('advisorLogin.html', msg = msg)

@app.route('/hod_dashboard')
def renderHodDashboardPage():
    return render_template('hodDashboard.html')

@app.route('/advsor_dashboard')
def renderAdvisorDashboardPage():
    return render_template('advisorDashboard.html')

@app.route('/coursesListingHod')
def renderHodShowAllCoursesPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM courses')
    data=cursor.fetchall()
    cursor.close()
    return render_template('hod_showAllCourses.html', courses = data)

@app.route('/studentsListingHod')
def renderHodShowAllStudentsPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM students')
    data = cursor.fetchall()
    cursor.close()

    # Group students by class
    students_by_class = {}
    for student in data:
        student_class = student['studentProgram']  # Assuming 'studentProgram' is the field representing the class
        if student_class not in students_by_class:
            students_by_class[student_class] = []
        students_by_class[student_class].append(student)

    return render_template('hod_showAllStudents_by_class.html', students_by_class=students_by_class)

@app.route('/classesListingHod')
def renderHodShowAllClassesPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM classRecords')
    data = cursor.fetchall()
    cursor.close()

    # Group students by class
    students_by_class = {}
    for student in data:
        student_class = student['class']  # Assuming 'studentProgram' is the field representing the class
        if student_class not in students_by_class:
            students_by_class[student_class] = []
        students_by_class[student_class].append(student)

    return render_template('hod_showAllClasses.html', students_by_class=students_by_class)

@app.route('/classesListingAdvisor')
def renderAdvisorShowAllClassesPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM classRecords')
    data = cursor.fetchall()
    cursor.close()

    # Group students by class
    students_by_class = {}
    for student in data:
        student_class = student['class']  # Assuming 'studentProgram' is the field representing the class
        if student_class not in students_by_class:
            students_by_class[student_class] = []
        students_by_class[student_class].append(student)

    return render_template('advisor_showAllClasses.html', students_by_class=students_by_class)

@app.route('/classesListingTeacher')
def renderTeacherShowAllClassesPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = session['user']
    teacher_name = data['teacherName']
    cursor.execute('SELECT * FROM classRecords where teacher = %s', (teacher_name,))
    data = cursor.fetchall()
    cursor.close()

    # Group students by class
    students_by_class = {}
    for student in data:
        student_class = student['class']  # Assuming 'studentProgram' is the field representing the class
        if student_class not in students_by_class:
            students_by_class[student_class] = []
        students_by_class[student_class].append(student)

    return render_template('teacher_showAllClasses.html', students_by_class=students_by_class)

@app.route('/leaveHistoryTeacher')
def renderTeacherShowLeaveHistoryPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = session['user']
    teacher = data['teacherName']
    cursor.execute('SELECT * FROM leaverequests where teacherName = %s ORDER BY approved_by_teacher ASC', (teacher,))
    data=cursor.fetchall()
    cursor.close()
    return render_template('teacher_showLeaveRequests.html', leaves = data)

@app.route('/leaveHistoryAdvisor')
def renderAdvisorShowLeaveHistoryPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = session['user']
    cursor.execute('SELECT * FROM leaverequests ORDER BY approved_by_advisor ASC')
    data=cursor.fetchall()
    cursor.close()
    return render_template('advisor_showLeaveRequests.html', leaves = data)

@app.route('/teachersListingHod')
def renderHodShowAllTeachersPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM teachers')
    data=cursor.fetchall()
    cursor.close()
    return render_template('hod_showAllTeachers.html', teachers = data)

@app.route('/leaveHistoryHod')
def renderHodShowLeaveRequestsPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM leaverequests ORDER BY approved_by_hod ASC')
    data=cursor.fetchall()
    cursor.close()
    return render_template('hod_showLeaveRequests.html', leaves = data)

@app.route('/approveLeavesAdvisor/<string:id>', methods=['POST'])
def approve_leave_advisor(id):

    dbb = MySQLdb.connect(host="localhost", 
    user="root", 
    passwd="", 
    db="lmsdb") 
    curb = dbb.cursor()
    curb.execute("UPDATE leaverequests SET approved_by_advisor = %s WHERE id = %s", (True, id,))
    dbb.commit()

    sid = request.form['studentId']
    curb = dbb.cursor()
    curb.execute("UPDATE classrecords SET allowedLeaves = allowedLeaves - 1 WHERE studentid = %s AND EXISTS (SELECT 1 FROM leaveRequests WHERE id = %s AND approved_by_teacher = TRUE AND approved_by_hod = TRUE);", (sid,id))
    dbb.commit()
    
    curb.close()

    return redirect('/leaveHistoryAdvisor')

# Route for the approving leave by hod
@app.route('/approveLeavesHod/<string:id>', methods=['POST'])
def approve_leave(id):

    dbb = MySQLdb.connect(host="localhost", 
    user="root", 
    passwd="", 
    db="lmsdb") 
    curb = dbb.cursor()
    curb.execute("UPDATE leaverequests SET approved_by_hod = %s WHERE id = %s", (True, id,))
    dbb.commit()

    sid = request.form['studentId']
    curb = dbb.cursor()
    curb.execute("UPDATE classrecords SET allowedLeaves = allowedLeaves - 1 WHERE studentid = %s AND EXISTS (SELECT 1 FROM leaveRequests WHERE id = %s AND approved_by_teacher = TRUE AND approved_by_advisor = TRUE);", (sid,id))
    dbb.commit()
    curb.close()

    return redirect('/leaveHistoryHod')

# Route for the approving leave by teacher
@app.route('/approveLeavesTeacher/<string:id>', methods=['POST'])
def approve_leave_teacher(id):

    dbb = MySQLdb.connect(host="localhost", 
    user="root", 
    passwd="", 
    db="lmsdb") 
    curb = dbb.cursor()
    curb.execute("UPDATE leaverequests SET approved_by_teacher = %s WHERE id = %s", (True, id,))
    dbb.commit()

    sid = request.form['studentId']
    curb = dbb.cursor()
    curb.execute("UPDATE classrecords SET allowedLeaves = allowedLeaves - 1 WHERE studentid = %s AND EXISTS (SELECT 1 FROM leaveRequests WHERE id = %s AND approved_by_hod = TRUE AND approved_by_advisor = TRUE);", (sid,id))
    dbb.commit()
    curb.close()

    return redirect('/leaveHistoryTeacher')


@app.route('/deleteLeaves/<string:leave_id>', methods=['POST'])
def delete_leave(leave_id):
    sName = request.form['studentName']
    sid = request.form['studentId']
    date = request.form['requestedAt']
    teacherName = request.form['teacherName']
    
    dbb = MySQLdb.connect(host="localhost", 
       user="root", 
       passwd="", 
       db="lmsdb") 
    curb = dbb.cursor()
    curb.execute("UPDATE leaverequests SET final_status = %s WHERE id = %s", ('rejected', leave_id,))
    dbb.commit()

    curb.execute("select studentEmail from students WHERE studentID = %s", (sid,))
    dbb.commit()
    student_email = curb.fetchone()[0]
    curb.close()
    
    message = "Hello "+sName+"!\n"+ "Your leave requested at "+date+ " is rejected by " +teacherName;
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(senderEmail,appPassword)
    server.sendmail(senderEmail,student_email,message)
    return redirect('/leaveHistoryTeacher')
###################################################################################################################
@app.route('/student_applyForLeave')
def renderStudentApplyForLeavePage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = session['user']
    studentId = data['studentID']
    studentName= data['studentName']
    cursor.execute('SELECT teacher from classRecords where studentid = %s', (studentId,))
    teachers=cursor.fetchall()
    cursor.execute('SELECT allowedLeaves from classRecords where studentid = %s', (studentId,))
    leaves = cursor.fetchone()
    cursor.close()
    return render_template('student_applyForLeave.html', 
                           teachers = teachers, leaves = leaves, studentId = studentId, studentName=studentName)

@app.route('/requestLeave', methods=['POST'])
def requestLeave():
    # Get form data
    studentID = request.form['studentId']
    studentName = request.form['studentName']
    teacherName = request.form['teacherName']
    numDays = request.form['numDays']
    requestedAt = datetime.today()

    certificate = request.files['medicalCertificate'].read()

    # Insert data into the 'leaverequests' table
    dbb = MySQLdb.connect(host="localhost", user="root", passwd="", db="lmsdb")
    curb = dbb.cursor()

    curb.execute("""
            INSERT INTO leaverequests (studentId,studentName,teacherName,numDays,requestedAt,approved_by_teacher,approved_by_advisor,approved_by_hod,final_status, medicalCertificate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (studentID, studentName, teacherName, numDays, requestedAt, False, False, False, "pending", certificate))
    dbb.commit()
    curb.close()
    return redirect(url_for('renderStudentShowLeaveHistoryPage'))


@app.route('/leaveHistoryStudent')
def renderStudentShowLeaveHistoryPage():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = session['user']
    studentId = data['studentID']
    cursor.execute('SELECT * FROM leaverequests where studentId = %s', (studentId,))
    data=cursor.fetchall()
    cursor.close()
    return render_template('student_showLeavesHistory.html', leaves = data)

@app.route('/download_certificate/<int:certificate_id>', methods=['GET'])
def download_certificate(certificate_id):
    try:
        # Connect to the database
        db = MySQLdb.connect(host="localhost", user="root", passwd="", db="lmsdb")
        cursor = db.cursor()

        # Fetch the file path from the database based on the certificate_id
        cursor.execute("SELECT medicalCertificate FROM leaverequests WHERE id = %s", (certificate_id,))
        result = cursor.fetchone()
        

        if result:
            # Assuming 'medicalCertificate' is the name of the column storing the file paths
            pdf_stream = io.BytesIO(result[0])

        # Return the PDF as a file attachment
            return send_file(pdf_stream, mimetype='application/pdf')
        else:
            # If certificate is not found
            return None

    except Exception as e:
        # Handle exceptions
        print("Error:", e)
        return None

    finally:
        # Close the database connection
        if db:
            db.close()


if __name__ == '__main__':
    app.run(debug=True)

@app.after_request
def add_header(response):
    response = app.response_class(response="", status=200)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response