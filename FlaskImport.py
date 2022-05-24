from flask import *
from flask_mysqldb import MySQL
from datetime import date
import csv
import hashlib
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'ninestar-db.cobd8enwsupz.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'adminpass'
app.config['MYSQL_DB'] = 'project_db'
 
mysql = MySQL(app)
app.secret_key = "abc"  


@app.route('/functions')

# Returns the hash of a string to store our passwords with
def hashp(passw):
    return hashlib.sha512(passw.encode('utf-8')).hexdigest()
    
# Takes in a UserID and a password and returns True if it is the users password in the database
def comparePassw(userID, passw):
    conn = mysql.connection
    mycursor = conn.cursor()
    sql = "SELECT UserPasswordID FROM users WHERE UserID = %s"
    val = (userID,)
    mycursor.execute(sql, val)
    
    sql = "SELECT PasswordString FROM passwords WHERE PasswordID = %s"
    val = (mycursor.fetchone()[0],)
    mycursor.execute(sql, val)
    
    if mycursor.fetchone()[0] == hashp(passw):
        return True
    else:
        return False

def get_id(username):
    conn = mysql.connection
    mycursor = conn.cursor()
    # mycursor = mysql.connection().cursor()
    selectID = "SELECT UserID FROM users WHERE UserName = %s"
    mycursor.execute(selectID, (username,))
    r = mycursor.fetchone()
    if r == None:
        return None
    else:
        return r[0]


def change_passw(passw, passID):
    conn = mysql.connection
    mycursor = conn.cursor()
    sql = "UPDATE passwords SET PasswordString = %s WHERE PasswordID = %s"
    val = (hashlib.sha512(passw.encode('utf-8')).hexdigest() , passID)
    mycursor.execute(sql, val)
    mysql.connection.commit()

# def get_username(userid):
#     mycursor = mysql.connection().cursor()
#     selectUN = "SELECT UserName FROM users WHERE UserID = %s"
#     mycursor.execute(selectUN, (userid,))
#     return mycursor.fetchone()[0]

# def get_date():
#     now = datetime.now()
#     return now.strftime("%Y-%m-%d")
    
# def get_points(userid):
#     mycursor = mysql.connection().cursor()
#     selectP = "SELECT UserPoints FROM users WHERE UserID = %s"
#     mycursor.execute(selectP, (userid,))
#     return mycursor.fetchone()[0]
    

# # Function List

# #   Checks UserType
# # admin_check(UserID) return T/F
# # sponsor_check(UserID) return T/F
# # driver_check(UserID) return T/F

# #   Checks Exsistance
# # user_check(UserName) return T/F   Checks for user in DB

# # Admin check to be called in files that need an admin to use
def admin_check(id):
    conn = mysql.connection
    mycursor = conn.cursor()
    sql = "SELECT UserTypeID FROM users WHERE UserID = %s"
    mycursor.execute(sql, (id,))
    if mycursor.fetchone()[0] == 3:
        return True
    else:
        return False
# # Sponsor check to be called in files that need a sponsor to use
def sponsor_check(id):
    conn = mysql.connection
    mycursor = conn.cursor()
    sql = "SELECT UserTypeID FROM users WHERE UserID = %s"
    mycursor.execute(sql, (id,))
    if mycursor.fetchone()[0] == 2:
        return True
    else:
        return False
# # Driver check to be called in files that need a driver to use
def driver_check(id):
    conn = mysql.connection
    mycursor = conn.cursor()
    sql = "SELECT UserTypeID FROM users WHERE UserID = %s"
    mycursor.execute(sql, (id,))
    if mycursor.fetchone()[0] == 1:
        return True
    else:
        return False

# # Checks that the given user exists given username
# def user_check(username):
#     mycursor = mysql.connection().cursor()
#     sql = "SELECT UserID FROM users WHERE UserName = %s"
#     mycursor.execute(sql, (username,))
#     if mycursor.fetchone():
#         return True
#     else:
#         return False
        
# def check_security(uid, answer):
#     mycursor = mysql.connection().cursor()
#     val = (uid,)
#     sql = "SELECT passwords.SecurityAnswer FROM passwords INNER JOIN users ON passwords.PasswordID = users.UserPasswordID WHERE users.UserID = %s"
#     mycursor.execute(sql, val)
#     if mycursor.fetchone()[0] == hashp(answer):
#         return True
#     else:
#         return False
# # Data manipulation

# # Don't forget to connection.commit() in calling file
# def add_points(userid, points):
#     mycursor = mysql.connection().cursor()
#     sql = "UPDATE users SET UserPoints = UserPoints + %s WHERE UserID = %s"
#     mycursor.execute(sql, (points, userid))

# def sub_points(userid, points):
#     mycursor = mysql.connection().cursor()
#     sql = "UPDATE users SET UserPoints = UserPoints - %s WHERE UserID = %s"
#     mycursor.execute(sql, (points, userid))
    
# def log_points(userid, points, reason, manid):
#     mycursor = mysql.connection().cursor()
#     mycursor.execute("SELECT UserPoints FROM users WHERE UserID = %s", (userid,))
#     totalPoints = mycursor.fetchone()[0]
#     pointLog = "INSERT INTO points(PointDate, PointReason, PointChange, PointDriverID, PointSponsorID, PointTotal) VALUES(%s, %s, %s, %s, %s, %s)"
#     mycursor.execute(pointLog, (get_date(), reason, points, userid, manid, totalPoints))
