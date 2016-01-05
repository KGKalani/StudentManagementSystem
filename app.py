''' <header>
<title>app.py</title>
<description>This is used to get all rquest send response back and manage all the functionalities</description>
<copyRight>Copyright (c) 2015</copyRight>
<createdOn>2015-12-31</createdOn>
<author>Gayathri Kalani</author>
</header>
'''
#!flask/bin/python
from flask import Flask, jsonify,abort,render_template,request,json
from models import Login,Teacher, Admin, Student
from pipelines import DataPipeline

app = Flask(__name__)

DataPipelineObj = DataPipeline() # DataPipeline object

@app.route('/')
def home():
     return render_template('home.html')

@app.route('/student_management_system/admin')
def adminPage():
    return render_template("adminPage.html")

@app.route('/student_management_system/teacher')
def teacherPage():
    return render_template("teacherPage.html")

@app.route('/student_management_system/student')
def studentPage():
    return render_template("studentPage.html")

#Sign in page render
@app.route('/student_management_system/showSignIn')
def showSignIn():
    return render_template('showSignIn.html')

#Function to user loggin
@app.route('/student_management_system/userloggin', methods = ['POST'])
def signIn():
     try:
        username = request.json['username']
        userPassword = request.json['userPassword']

        result = DataPipelineObj.fetch_login_data_for_login() #fetch data from login table in the database

        for row in result:
            if (username == row['username']): #if usernames are matched
                if (userPassword == row['password']): #if passwords are matched
                    return row['user_type']
                else:       #if passwords are not matched
                    return "Password is incorrect"

        return "login failed"

     except:    #if required details are not filled
         return "Filled required details"


#Sign up page render
@app.route('/student_management_system/showSignUp')
def showSignUp():
    return render_template('showSignUp.html')

#Function to signup
@app.route('/student_management_system/userSignUp', methods = ['POST'])
def signUp():
         try:
            username        = request.json['username']
            userPassword    = request.json['userPassword']
            userNIC         = request.json['userNIC']
            userType        = request.json['userType']

            result  = DataPipelineObj.fetch_data(userType) #fetch data
            newUser = Login(username, userPassword,userType) #Create new user
            newPerson = ""
            for row in result:
                if(userNIC == row['nic']):  #if already registered person
                    result1 = DataPipelineObj.fetch_login_data(userType) #fetch login data from the database

                    for row1 in result1:
                        if username == row1['username']: #if username already exists
                            return "Username already exists"

                    DataPipelineObj.insert_signup_data(newUser) #if new user insert data to the database
                    DataPipelineObj.update_table(userType,username,userNIC)

                    return "Sign up successfully"

            return "You are not a registered user"  # if not registred person
         except:
            return "Fill the required details" #if required details are not filled


#Teacher and admin registration page render
@app.route('/student_management_system/showOtherUserRegistration')
def registerOtherUsers():
    return render_template('OtherUsersRegistrationPage.html')

#Function to register teachers and admin
@app.route('/student_management_system/otherUsersRegistration', methods = ['POST'])
def otherUserRegistration():
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

        DataPipelineObj.insert_signup_data(newUser) #Add details to the database
        return "Registered successfully"

    except:
        return "Fill the required details"


#Student registration page render
@app.route('/student_management_system/showStudentRegistration')
def registerStudents():
    return render_template('studentRegistration.html')

#Function to register students
@app.route('/student_management_system/studentRegistration', methods = ['POST'])
def studentRegistration():
    try:
        userId  = request.json['user_id']
        name    = request.json['name']
        grade   = request.json['grade']
        student = Student(userId, name, grade)

        newUser = Login(userId, userId,"student") #Create new user
        DataPipelineObj.insert_signup_data(newUser) #Add details to the database (Into login table)

        DataPipelineObj.insert_signup_data(student)#Add details to the database(Into Student table

        return "Registered successfully"

    except:
        return "Fill the required details"


if __name__ == '__main__':
    app.run(debug=True)