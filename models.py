''' <header>
<title>models.py</title>
<description>Create all models.database connectionc, data insert and classes</description>
<copyRight>Copyright (c) 2015</copyRight>
<createdOn>2015-12-31</createdOn>
<author>Gayathri Kalani</author>
</header>
'''

from  sqlalchemy import create_engine, Column, String, Integer, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy.engine.url import URL
from sqlalchemy.orm.collections import prepare_instrumentation

import settings

DeclarativeBase = declarative_base()

def connect_database():
    return create_engine(URL(**settings.DATABASE))

#Create all tables in the the engine. This is equivalent to "Create Table" statements in rqw SQL
def create_data_table(engine):
    DeclarativeBase.metadata.create_all(engine)

#Bind the engine to the method of the Base class so that the declaratives can be accessed through a DBSession instance
def insert_data(engine):
    DeclarativeBase.metadata.bind = engine


#Class for login
class Login(DeclarativeBase):
    __tablename__ = 'login'

    username = Column(String(20), primary_key= True)
    password = Column(String(20))
    user_type = Column(String(20))

    def __init__(self,username, password, userType):
        self.username = username
        self.password = password
        self.user_type = userType

#Class for teacher
class Teacher(DeclarativeBase):
    __tablename__ = 'teacher'

    id = Column(String(20), primary_key= True)
    name = Column(String(20))
    nic = Column(String(10))
    username = Column(String(20))

    def __init__(self,t_id, name, NIC):
        self.id = t_id
        self.name = name
        self.nic  = NIC

#Class for Admin
class Admin(DeclarativeBase):
    __tablename__ = 'admin'

    id = Column(String(20), primary_key= True)
    name = Column(String(20))
    nic = Column(String(10))
    username = Column(String(20))

    def __init__(self,admin_id, name, NIC):
        self.id = admin_id
        self.name = name
        self.nic  = NIC

#Class for student
class Student(DeclarativeBase):
    __tablename__ = 'student'

    id = Column(String(20), primary_key= True)
    name = Column(String(20))
    grade = Column(Integer)
    username = Column(String(20))

    def __init__(self,s_id, name, grade):
        self.id = s_id
        self.name = name
        self.grade  = grade
        self.username = s_id

#Class for tution class
class Class(DeclarativeBase):
    __tablename__ = 'tution_class'

    class_id = Column(String(20),primary_key=True)
    grade = Column(Integer)
    subject = Column(String(20))

    def __init__(self,class_id, grade, subject):
        self.class_id = class_id
        self.grade  = grade
        self.subject = subject


#class for schedule
class Schedule(DeclarativeBase):
    __tablename__ = 'schedule'

    schedule_id = Column(String(20),primary_key=True)
    day = Column(String(20))
    start_time = Column(Time)
    end_time = Column(Time)

    def __init__(self, schedule_id, day, start_time, end_time):
        self.schedule_id = schedule_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

#class for class_schedule
class Class_schedule(DeclarativeBase):
    __tablename__ = 'class_schedule'

    class_id = Column(String(20), ForeignKey("tution_class.class_id"),primary_key=True)
    schedule_id = Column(String(20), ForeignKey("schedule.schedule_id"),primary_key=True)

    def __init__(self, class_id, schedule_id):
        self.class_id = class_id
        self.schedule_id = schedule_id

#Class for teacher_class
class Teacher_class(DeclarativeBase):
    __tablename__ = 'teacher_class'

    id = Column(String(20),ForeignKey("teacher.id"),primary_key= True)
    class_id = Column(String(20), ForeignKey("tution_class.class_id"), primary_key=True)

    def __init__(self, t_id, class_id):
        self.class_id = class_id
        self.id = t_id

#Class for student_class table
class Student_class(DeclarativeBase):
    __tablename__ = 'student_class'

    id = Column(String(20),ForeignKey("student.id"),primary_key=True)
    class_id = Column(String(20),ForeignKey("tution_class.class_id"), primary_key=True)

    def __init__(self,s_id, class_id):
        self.id = s_id
        self.class_id = class_id
