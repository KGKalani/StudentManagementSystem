''' <header>
<title>DataPipeline</title>
<description>This is used to add, fetch, update and delete data in the database using sqlalchemy</description>
<copyRight>Copyright (c) 2015</copyRight>
<createdOn>2015-12-31</createdOn>
<author>Gayathri Kalani</author>
</header>
'''
from sqlalchemy.orm import sessionmaker
from models import connect_database,create_data_table,insert_data, Teacher, Admin, Login

class DataPipeline():
    def __init__(self):
        self.engine = connect_database()
        insert_data(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_signup_data(self, user):
        #Insert a new user in the login table
        try:
            self.session.add(user)
            self.session.commit()
        except:
            self.session.rollback()
            raise


    #fetch data from teacher or admin tables based on NIC
    def fetch_data(self, tableName,userNIC):
        result = ""
        if(tableName == 'teacher'):
            result = self.session.query(Teacher).filter_by(nic = userNIC)
        if(tableName == 'admin'):
            result = self.session.query(Admin).filter_by(nic = userNIC)

        return result

    #fetch data from login table using userType
    def isUsernameExists(self, userType, username):
        result = self.session.query(Login).filter_by(user_type = userType).filter_by(username = username)
        return result

    #fetch data from login table to check valid user or not
    def isValidUser(self, username, password):
        result = self.session.query(Login).filter_by(username = username).filter_by(password = password)
        return result


    #update user tables(teacher and admin)
    def update_table(self, user,username):
        try:
            user.username = username
            self.session.commit()
            return "Success"
        except:
            return "Fail"
        finally:
            self.session.close()

    def fetch_data_from_usertable(self,userType,username):
        user = ""
        if(userType == 'teacher'):
            user = self.session.query(Teacher).filter(Teacher.username == username).one()

        if(userType == 'admin'):
            user = self.session.query(Admin).filter(Admin.username == username).one()

        return user