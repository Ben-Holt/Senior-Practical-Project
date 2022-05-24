# from __main__ import app
from FlaskImport import *
from home import home

@app.route('/sponsor_deny', methods = ['POST', 'GET'])
def sponsor_deny():
    uid = session['uid']

    if request.method == 'POST':
        driver = request.form['driver']
        reason= request.form['reason']
        cursor = mysql.connection.cursor()

        val = (uid,)
        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s"
        cursor.execute(sql, val)
        orgName = cursor.fetchone()[0]

        val = (driver, orgName)
        sql = "SELECT ApplicationID FROM applications WHERE ApplicationDriverName = %s AND ApplicationSponsorName=%s"
        cursor.execute(sql, val)
        appid = cursor.fetchone()[0]

        sql = "UPDATE applications SET ApplicationStatus = %s WHERE ApplicationID = %s"
        val = ('denied', appid)
        cursor.execute(sql, val)

        sql = "UPDATE applications SET ApplicationReason = %s WHERE ApplicationID = %s"
        val = (reason, appid)
        cursor.execute(sql, val)

        mysql.connection.commit()
        return home()
