# from __main__ import app
from FlaskImport import *
from points_admin import points_admin
from points_driver import points_driver

@app.route('/points_check')
def points_check():
    if admin_check(session['uid']) == True:
        return points_admin()
     
    if driver_check(session['uid']) == True:
        return points_driver()