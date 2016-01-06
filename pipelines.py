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
        #create_data_table(self.engine)
        insert_data(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def insert_signup_data(self, user):
        # A DBSession() instance establishes all conversations with the database and represents a "staging zone" for
        # all the objects loaded into the database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call session.commit(). If you're not happy about the
        # changes, you can revert all of them back to the last commit by calling session.rollback()
        #session = self.Session()

        #Insert a new user in the login table
        try:
            self.session.add(user)
            self.session.commit()
        except:
            self.session.rollback()
            raise

    #fetch data from teacher or admin tables
    def fetch_data(self, tableName):
        result = ""
        if(tableName == 'teacher'):
            result = self.session.query(Teacher)
        if(tableName == 'admin'):
            result = self.session.query(Admin)

        return result

    #fetch data from login table useing userType
    def fetch_login_data(self,userType):
        result = self.session.query(Login).filter(Login.user_type == userType)
        #query = "select *from login where user_type = '"+userType+"'"
        #result = self.engine.execute(query)
        return result

    #fetch data from login table
    def fetch_login_data_for_login(self):
        result = self.session.query(Login)
        #query = "select *from login"
        #result = self.engine.execute(query)
        return result


    def update_table(self, user,username):
        try:
            user.username = username
            self.session.commit()
            #query = "update "+userType+" set username = '"+username+"' where nic = '"+NIC+"'"
            #result = self.engine.execute(query)
            return "Success"
        except:
            return "Fail"
