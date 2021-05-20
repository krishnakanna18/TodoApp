from flask_restplus import Api, Resource, fields, reqparse, Namespace
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user
from flask_user import login_required
import pymysql

connection = pymysql.connect(host='localhost',
                             user='krishna',
                             password='0mysqldb@Krishna',
                             database='todo',
                             cursorclass=pymysql.cursors.DictCursor)

'''
+----------+--------------+------+-----+---------+-------+
| Field    | Type         | Null | Key | Default | Extra |
+----------+--------------+------+-----+---------+-------+
| username | varchar(200) | NO   | PRI | NULL    |       |
| password | varchar(200) | NO   |     | NULL    |       |
| role     | varchar(20)  | YES  |     | read    |       |
+----------+--------------+------+-----+---------+-------+
'''

login_manager = LoginManager()

ns1=Namespace('user',description="User authentication and authorization")

user=ns1.model('users',{
    'username':fields.String(required=True,description='Unique username of the user'),
    'password':fields.String(required=True,description='Password of the user'),
    'role':fields.String(required=True,description="Read or Write access. Can take values- 'read' or 'write'",default='read')
})

#User class for session storage and user details
class User(UserMixin):
    def __init__(self,data,active=True):
        self.username=data['username']
        self.password=data['password']
        try:
            self.role=data['role']
        except:
            self.role='read'
        self.active = active

    def get_id(self):
        return self.username

    def is_active(self):
        return self.active

    def __str__(self):
        return self.username

#Helper class for db operations
class UserHelper(object):

    def get(self,username):         #Get user with username
        #Create a cursor for querying db
        cursor=connection.cursor()
        sql="select * from user where username=%s"
        cursor.execute(sql,(username))
        user=cursor.fetchone()
        cursor.close()
        return user

    def create(self,user):         #Create user 
        cursor=connection.cursor()
        sql="insert into user values(%s,%s,%s)"
        cursor.execute(sql,(user['username'],user['password'],user['role']))
        cursor.close()
        connection.commit()


userHelper=UserHelper()

@login_manager.user_loader
def load_user(username):
    return User(userHelper.get(username))


@ns1.route('/login',methods=['POST'])
class userLogin(Resource):

    @ns1.expect(user)
    def post(self):
        user=userHelper.get(ns1.payload['username'])
        if(user==None):
            return {"message":"Username not found"},401
        if(user['password']!=ns1.payload['password']):
            return {"message":"Invalid password"},401
        login_user(User(user))
        return {"message":"Success"},200

@ns1.route('/logout',methods=['POST'])
class userLogout(Resource):

    def post(self):
        logout_user()
        return {"message":"Success"},200
