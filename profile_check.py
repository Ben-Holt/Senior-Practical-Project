# from __main__ import app
from FlaskImport import *
from profile_page_admin import profile_admin
from profile_page_driver import profile_driver
from profile_page_sponsor import profile_sponsor

@app.route('/profile_check')
def profile_check():
    if admin_check(session['uid']) == True:
        return profile_admin()
     
    if driver_check(session['uid']) == True:
        return profile_driver()
             
    if sponsor_check(session['uid']) == True:
        return profile_sponsor()