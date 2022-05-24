from FlaskImport import *


@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('login.html')

 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET': 
        return render_template('login.html')
     
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        uid = get_id(username)

        if (uid == "" or password == ""):
            return render_template('login.html', err='Invalid. Try Again')
        cursor = mysql.connection.cursor()

        if (uid != None):
            if comparePassw(uid, password) :
                session['uid'] = uid

                sql = "INSERT INTO logins (LoginUsername, LoginDate, LoginSuccessful) VALUES (%s,%s,%s)"
                val = (username, date.today(), 'Success')
                cursor.execute(sql, val)
                mysql.connection.commit()
                cursor.close()

                return home()
            else :
                sql = "INSERT INTO logins (LoginUsername, LoginDate, LoginSuccessful) VALUES (%s,%s,%s)"
                val = (username, date.today(), 'Failure')
                cursor.execute(sql, val)
                mysql.connection.commit()
                cursor.close()
                return render_template('login.html', err='Invalid. Try Again')
        else:
            sql = "INSERT INTO logins (LoginUsername, LoginDate, LoginSuccessful) VALUES (%s,%s,%s)"
            val = (username, date.today(), 'Failure')
            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()
            return render_template('login.html', err='Bad Username')

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    session.pop('uid', None)
    session.pop('changeid', None)
    return render_template('login.html')


from user_change_name import *
from user_change_contact_info import *
from profile_page_admin import *
from profile_page_driver import *
from profile_page_sponsor import *
from profile_check import *
from apply import *
from sponsor_apply_page import *
from catalog import *
from home import *
from change_points import *
from points_check import *
from points_admin import *
from items import *
from driver_cart import *
from driver_cart_remove import *
from cart_checkout import *
from create_account import *
from create_sponsor import *
from create_admin import *
from forgot_password import *
from change_password import *
from admin_pair import *
from auditLog import *
from auditLog_sponsor import *
from report_driver_points import *
from report_driver_points_all import *
from change_fee_ratio import *
from report_sales_by_sponsor import *
from report_sales_by_driver import *
from report_invoice import *
from sponsor_deny import *
from driver_view import *
from sponsor_view import *

app.run(host='0.0.0.0', port=8080)
#app.run(host='localhost', port=5000)
