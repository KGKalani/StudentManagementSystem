''' <header>
<title>app.py</title>
<description>This is used to get all rquest send response back and manage all the functionalities</description>
<copyRight>Copyright (c) 2015</copyRight>
<createdOn>2015-12-31</createdOn>
<author>Gayathri Kalani</author>
</header>
'''
#!flask/bin/python
import json

from flask import Flask, jsonify,abort,render_template,request,session

from models import Login,Teacher, Admin, Student, Class, Teacher_class, Schedule, Class_schedule,Student_class
from pipelines import DataPipeline

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyofstudentmanagementsystem'

DataPipelineObj = DataPipeline() # DataPipeline object

@app.route('/')
def home():
    session['logged_in'] = False
    return render_template('home.html')

@app.route('/student_management_system/admin')
def adminPage():
    if(session['logged_in'] == True):
        return render_template("adminPage.html")

@app.route('/student_management_system/teacher')
def teacherPage():
    if(session['logged_in'] == True):
        return render_template("teacherPage.html")

@app.route('/student_management_system/student')
def studentPage():
    if(session['logged_in'] == True):
        return render_template("studentPage.html")


#Function to signup
@app.route('/student_management_system/userSignUp', methods = ['GET', 'POST'])
def signUp():
    if(request.method == 'GET'):
        return render_template('showSignUp.html')

    elif(request.method == 'POST'):
         DataPipelineSignUpObj = DataPipeline() # DataPipeline object
         try:
            username        = request.json['username']
            userPassword    = request.json['userPassword']
            userNIC         = request.json['userNIC']
            userType        = request.json['userType']

            user  = DataPipelineSignUpObj.fetch_data(userType,userNIC) #fetch data
            newLoginUser = Login(username, userPassword,userType) #Create new user

            if(user.count() != 0):
                result = DataPipelineSignUpObj.isUsernameExists(userType, username) #fetch login data from the database

                if(result.count() != 0): #if usernae alredy exists
                    return jsonify({'status':"Username already exists"})

                DataPipelineSignUpObj.insert_data(newLoginUser) #if new user insert data to the database
                for u in user:
                    DataPipelineSignUpObj.update_table(u,username) #update the user tables(teacher and admin)

                return jsonify({'status':"Sign up successfully"})

            return jsonify({'status':"You are not a registered user"})  # if not registred person
         except:
            return jsonify({'status':"Fill the required details"}) #if required details are not filled

    else:
        abort(405)


#Function to user loggin
@app.route('/student_management_system/userloggin', methods = ['GET', 'POST'])
def signIn():
    if(request.method == 'GET'):
        return render_template('showSignIn.html')

    elif(request.method == 'POST'):
        try:
            username = request.json['username']
            userPassword = request.json['userPassword']

            user = DataPipelineObj.isValidUser(username, userPassword) #fetch data from login table in the database
            if(user.count() == 1): #if valid user
                for u in user:
                    newUser = DataPipelineObj.fetch_data_from_usertable(u.user_type,u.username)
                    userDetails = {
                        'name': newUser.name,
                        'username': newUser.username,
                        'type': u.user_type,
                        'nic': newUser.nic
                    }
                    session['logged_in'] = True         # new sessions for user
                    session['user_id'] = newUser.id
                    session['username'] = newUser.username
                    session['user_type'] = u.user_type

                    return jsonify(userDetails)

            return jsonify({'status':"Invalid loggin"})

        except:    #if required details are not filled
            return jsonify({'status':"Filled required details"})

    else:
        abort(405)

#Function to sign out users
@app.route('/student_management_system/signOut')
def signOut():
     session['logged_in'] = False
     session.pop('user_id',None)
     session.pop('username',None)
     session.pop('user_type',None)
     return render_template('home.html')

#Function to register teachers and admin
@app.route('/student_management_system/otherUsersRegistration', methods = ['GET', 'POST'])
def otherUserRegistration():

    if(session['logged_in'] == True): #if user login
        if(request.method == 'GET'):
            return render_template('OtherUsersRegistrationPage.html')

        elif(request.method == 'POST'):
            try:
                userId      = request.json['user_id']
                name        = request.json['name']
                userNIC     = request.json['userNIC']
                userType    = request.json['userType']
                newUser     = ""

                if(userType == "teacher"): #if a teache, create new teacher object
                    newUser = Teacher(userId, name, userNIC)

                if(userType == "admin"): #if a admin create new admin object
                    newUser = Admin(userId, name, userNIC)

                DataPipelineObj.insert_data(newUser) #Add details to the database
                return jsonify({'status':"User successfully registered"})

            except:
                return jsonify({'status':"Fill the required details"})

        else:
            abort(405)
    else: #if user  not login
        return render_template('showSignIn.html')


#Function to register students
@app.route('/student_management_system/studentRegistration', methods = ['GET', 'POST'])
def studentRegistration():

    if(session['logged_in'] == True): #if user login
        if(request.method == 'GET'):
            return render_template('studentRegistration.html')

        elif(request.method == 'POST'):
            try:
                userId  = request.json['user_id']
                name    = request.json['name']
                grade   = request.json['grade']
                student = Student(userId, name, grade)

                newUser = Login(userId, userId,"student") #Create new user
                DataPipelineObj.insert_data(newUser) #Add details to the database (Into login table)

                DataPipelineObj.insert_data(student)#Add details to the database(Into Student table

                return jsonify({'status':"Student successfully registered"})

            except:
                return jsonify({'status':"Fill the required details"})
        else:
            abort(405)
    else: #if user not login
        return render_template('showSignIn.html')

#Function to class registration
@app.route('/student_management_system/classRegistration', methods = ['GET', 'POST'])
def classRegistration():

    if(session['logged_in']): #if user not loggin
        if(request.method == 'GET'):
            return render_template('classRegistration.html')

        elif(request.method == 'POST'):
            try:
                t_id = request.json['t_id']
                class_id = request.json['class_id']
                grade = request.json['grade']
                subject = request.json['subject']

                teacher = DataPipelineObj.get_teacher_details(t_id)

                if(teacher):                           #if there is a teacher with that id
                    newClass = Class(class_id, grade, subject)
                    new_teacher_class = Teacher_class(t_id, class_id)
                    DataPipelineObj.insert_data(newClass)            #add new class etails into the database
                    DataPipelineObj.insert_data(new_teacher_class)
                    return jsonify({'status':"Class successfully registered"}) #update teache_class table

                else:                                                #if there is not a teacher with that id
                    return jsonify({'status':"There is no such teacher id"})
            except:
                 return jsonify({'status':"There is something wrong. Check whether you have filled require details correctly"})

    else: #if user not login
        return render_template('showSignIn.html')

#Function to schedule registration
@app.route('/student_management_system/scheduleRegistration', methods = ['GET', 'POST'])
def scheduleRegistration():
    if(request.method == 'GET'):
        return render_template('classScheduleRegistration.html')

    if(request.method == 'POST'):
        try:
            class_id = request.json['class_id']
            schedule_id = request.json['schedule_id']
            day = request.json['day']
            start_time = request.json['start_time']
            end_time = request.json['end_time']

            newSchedule = Schedule(schedule_id, day, start_time, end_time)
            new_class_schedule = Class_schedule(class_id, schedule_id)
            DataPipelineObj.insert_data(newSchedule)                    #add new schedule to the database
            DataPipelineObj.insert_data(new_class_schedule)             #update class_schedule table
            return jsonify({'status':"Schedule successfully registered"}) #update teache_class table

        except:
             return jsonify({'status':"There is something wrong. Check whether you have filled require details correctly"})

#Function to get class details
@app.route('/student_management_system/getClassDetails', methods =['GET', 'POST'])
def getClassDetails():
    if request.method == 'GET':
        return render_template('classRegistrationsForStudents.html')

    if request.method == 'POST':
        try:
            grade = request.json['grade']
            subject = request.json['subject']

            class_details = []
            result = DataPipelineObj.get_class_Details(grade,subject) #get class details
            for u in result:
                t_id = u.id
                schedule_id = u.schedule_id
                teacher = DataPipelineObj.get_teacher_details(t_id)                     #get teachers details
                schedule = DataPipelineObj.get_schedule_Details(schedule_id)            #get schedule details

                details ={                                  #class details dectionary
                    'class_id': u.class_id,
                    'teacher_name':teacher.name,
                    'day':schedule.day,
                    'start_time':str(schedule.start_time),
                    'end_time':str(schedule.end_time)
                }

                class_details.append(details)       #add class details into a list
                jsonObj = {                         #json object
                    'statusCode': 100,
                    'status': 'OK',
                    'data':class_details
                }

            if len(class_details) != 0:         #if there is a class
                return jsonify(jsonObj)         #return class details

            else:               #if there is no classes
                return jsonify({'statusCode': 400,'status':"No classes"})
        except:
                return jsonify({'statusCode': 500, 'status':"There is something wrong. Check whether you have filled require details correctly"})

#Function to register students for classes
@app.route('/student_management_system/studentRegisterForClasses/<s_id>/<class_id>', methods =['POST'])
def student_management_system(s_id,class_id):
    try:
        student_class_obj = Student_class(s_id,class_id) #make an object
        DataPipelineObj.insert_data(student_class_obj)  #insert data into the database
        return jsonify({'status':"Class is registered successfully"})
    except:
        return jsonify({'status':"There is something wrong. Check whether you have filled require details correctly"})


if __name__ == '__main__':
    app.run(debug=True)