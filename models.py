''' <header>
<title>models.py</title>
<description>Create all models.database connectionc, data insert and classes</description>
<copyRight>Copyright (c) 2015</copyRight>
<createdOn>2015-12-31</createdOn>
<author>Gayathri Kalani</author>
</header>
'''

from  sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy.engine.url import URL

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

    t_id = Column(String(20), primary_key= True)
    name = Column(String(20))
    NIC = Column(String(10))
    username = Column(String(20))

    def __init__(self,t_id, name, NIC):
        self.t_id = t_id
        self.name = name
        self.NIC  = NIC

#Class for Admin
class Admin(DeclarativeBase):
    __tablename__ = 'admin'

    admin_id = Column(String(20), primary_key= True)
    name = Column(String(20))
    NIC = Column(String(10))
    username = Column(String(20))

    def __init__(self,admin_id, name, NIC):
        self.admin_id = admin_id
        self.name = name
        self.NIC  = NIC

#Class for student
class Student(DeclarativeBase):
    __tablename__ = 'student'

    s_id = Column(String(20), primary_key= True)
    name = Column(String(20))
    grade = Column(Integer)
    username = Column(String(20))

    def __init__(self,s_id, name, grade):
        self.s_id = s_id
        self.name = name
        self.grade  = grade
        self.username = s_id